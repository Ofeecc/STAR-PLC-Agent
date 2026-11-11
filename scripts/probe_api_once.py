"""Prepare a one-request compatibility probe; execution requires explicit approval.

Without --run this only validates local configuration and prints the request plan.
Use --run --allow-model-api only after the user approves this specific request.
"""
import argparse
from dataclasses import replace
import json

from plc_agent.common import ROOT, now, redact, write_json
from plc_agent.config import Settings
from plc_agent.llm import ProviderError, ResponsesClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='deepseek-v4.1-flash-1017')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--allow-model-api', action='store_true')
    args = parser.parse_args()
    if args.run and not args.allow_model_api:
        parser.error('Ask the user for this request first, then pass --allow-model-api')
    cfg = replace(Settings.load(load_api=True), reasoning_effort='low', llm_timeout=60)
    plan = {'model': args.model, 'endpoint': cfg.base_url.rstrip('/') + '/responses',
            'prompt': 'Reply with exactly OK.', 'max_output_tokens': 128,
            'maximum_requests': 1, 'automatic_retries': 0,
            'key_loaded': bool(cfg.api_key.strip()), 'mode': 'RUN' if args.run else 'LOCAL_CHECK_ONLY'}
    print(json.dumps(plan, ensure_ascii=False, indent=2), flush=True)
    if not cfg.api_key.strip() or not cfg.base_url:
        return 1
    if not args.run:
        return 0
    folder = ROOT / 'results/raw' / ('api_probe_' + now().replace(':', '').replace('.', ''))
    write_json(folder / 'plan.json', plan)
    try:
        reply = ResponsesClient(cfg).respond(args.model, [{'role': 'user', 'content': plan['prompt']}],
                                             folder, max_tokens=128, timeout=60)
        result = {'status': 'PASS' if reply['text'].strip() == 'OK' else 'UNEXPECTED_REPLY',
                  'requested_model': args.model, 'reported_model': reply.get('reported_model'),
                  'reply': redact(reply['text'], [cfg.api_key]), 'usage': reply.get('usage'),
                  'elapsed_seconds': reply.get('elapsed_seconds'), 'evidence_dir': str(folder)}
    except ProviderError as exc:
        result = {'status': 'TOOL_ERROR', 'error': redact(str(exc), [cfg.api_key]),
                  'evidence_dir': str(folder)}
    write_json(folder / 'probe_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
