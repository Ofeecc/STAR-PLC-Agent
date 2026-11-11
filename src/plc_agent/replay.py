"""Reuse exact completed requests when continuing an interrupted pilot run."""
import json
import shutil
from pathlib import Path

from .common import digest, now, read_json, write_json
from .llm import ProviderError, ResponsesClient


class ResumingClient(ResponsesClient):
    def __init__(self, settings, original_run, remaining_requests):
        super().__init__(settings)
        self.original_run=Path(original_run)
        self.remaining_requests=remaining_requests
        self.reused=[]

    def respond(self,model,input_items,log_dir,tools=None,tool_choice=None,max_tokens=None,timeout=None):
        log_dir=Path(log_dir)
        original=self.original_run/log_dir.name
        if log_dir.name in ('llm_planner','llm_code_00'):
            request=read_json(original/'request.json')
            response=read_json(original/'response.json')
            expected=(request['model']==model and digest(request['input'])==digest(input_items)
                      and request.get('tools')==tools and request.get('tool_choice')==tool_choice
                      and request.get('reasoning')=={'effort':self.settings.reasoning_effort}
                      and request.get('max_output_tokens')==(max_tokens or self.settings.max_output_tokens)
                      and response.get('status')=='completed')
            if not expected:
                raise ProviderError('Cached request differs; stopped before spending on a replacement')
            log_dir.mkdir(parents=True,exist_ok=False)
            for name in ('request.json','response.json','events.json','context.json'):
                if (original/name).is_file(): shutil.copy2(original/name,log_dir/name)
            write_json(log_dir/'reused_request.json',{'original':str(original),'new_request':False,'utc':now(),
                                                     'original_usage':response.get('usage')})
            self.reused.append(str(original))
            with (log_dir.parent/'model_calls.jsonl').open('a',encoding='utf-8') as stream:
                stream.write(json.dumps({'utc':now(),'event':'request_reused','call_dir':log_dir.name,
                                         'original':str(original),'new_request':False})+'\n')
            output=response.get('output',[])
            text=''.join(c.get('text','') for item in output if item.get('type')=='message'
                         for c in item.get('content',[]) if c.get('type')=='output_text')
            return {'text':text,'output':output,'usage':None,'reported_model':response.get('model'),
                    'elapsed_seconds':0,'reused':True}
        if self.request_count>=self.remaining_requests:
            raise ProviderError('Remaining request budget for resumed experiment exhausted')
        return super().respond(model,input_items,log_dir,tools,tool_choice,max_tokens,timeout)
