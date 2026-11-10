"""Complete input-driven reference transitions for three public process tasks."""
from .data_contracts import real32

SUPPORTED_PROCESS={'PUB015','PUB016','PUB020'}

class ProcessContract:
    def __init__(self,task_id):
        self.task_id=task_id;self.phase=0;self.mode=None;self.previous={}
        self.latches=[False]*5;self.batch_mode=None;self.route=None
        self.index=0;self.station=1;self.target=1;self.temperature=0.0

    def edges(self,i,names):
        result={n:i[n] and not self.previous.get(n,False) for n in names}
        self.previous.update({n:i[n] for n in names})
        return result

    def step(self,i):
        if self.task_id=='PUB015':return self.mixing(i)
        if self.task_id=='PUB016':return self.routing(i)
        if self.task_id=='PUB020':return self.production(i)
        raise ValueError('Unsupported process contract')

    def mixing(self,i):
        buttons=['valveAStart','valveBStart','valveCStart','valveDStart','mixMotorStart']
        outputs=['valveARun','valveBRun','valveCRun','valveDRun','mixMotorRun']
        edge=self.edges(i,buttons+['autoStart'])
        changed=self.mode is not None and self.mode!=i['opeMode'];self.mode=i['opeMode']
        if not i['estop'] or changed:
            self.phase=0;self.latches=[False]*5;self.batch_mode=None
            return dict.fromkeys(outputs,False)
        if not i['opeMode']:
            self.latches=[old!=edge[b] for b,old in zip(buttons,self.latches)]
            return dict(zip(outputs,self.latches))
        if self.phase in (1,2,3,4) and i['processMode']!=self.batch_mode:
            raise ValueError('processMode changed during batch outside declared domain')
        # IDLE, FILL_A, FILL_B, FILL_C, MIX, DRAIN. One branch per call.
        if self.phase==0 and edge['autoStart']:
            self.phase=1;self.batch_mode=i['processMode']
        elif self.phase==1 and i['levelSensor']>=50:self.phase=2
        elif self.phase==2 and i['levelSensor']>=80:self.phase=3 if self.batch_mode else 4
        elif self.phase==3 and i['levelSensor']>=100:self.phase=4
        elif self.phase==4 and i['mixMotorComplete']:self.phase=5
        return {n:self.phase==p for n,p in zip(outputs,[1,2,3,5,4])}

    def routing(self,i):
        edge=self.edges(i,['station1Start','station2Complete','station3Complete','station4Complete'])
        length=i['processLength'];sequence=i['processSequence']
        if type(length) is not int or not 1<=length<=8 or not isinstance(sequence,list) or len(sequence)!=8:
            raise ValueError('Invalid process sequence dimensions')
        active=tuple(sequence[:length])
        if any(type(s) is not int for s in active) or active[-1]!=5 or any(s not in (2,3,4) for s in active[:-1]):
            raise ValueError('Invalid active route')
        if self.phase and active!=self.route:raise ValueError('Active route changed during product cycle')
        # IDLE=0, MOVING=1, WAIT_PROCESS=2.
        if self.phase==0:
            if edge['station1Start'] and i['sensor1']:
                self.route=active;self.index=0;self.station=1;self.target=active[0];self.phase=1
        elif self.phase==1:
            if i['sensor'+str(self.target)]:
                self.station=self.target;self.phase=0 if self.target==5 else 2
        elif self.phase==2 and edge['station'+str(self.station)+'Complete']:
            self.index+=1;self.target=self.route[self.index]
            self.phase=2 if self.target==self.station else 1
        moving=self.phase==1 and not i['sensor'+str(self.target)]
        return dict(conveyorLeft=moving and self.target<self.station,
                    conveyorRight=moving and self.target>self.station)

    def production(self,i):
        # WAIT_FEED, MOVE_WASH, WAIT_WASH, MOVE_WEIGHT, WAIT_WEIGHT,
        # REJECT, MOVE_FIRING, WAIT_FIRING, MOVE_OUTPUT, OUTPUT_DONE.
        if not i['Mode']:
            self.phase=0
            return dict(MotorForward=i['ForwardButton'] and not i['ReverseButton'],
                        MotorReverse=i['ReverseButton'] and not i['ForwardButton'],
                        kick=False,CompletionLight=False,firingTemp=self.temperature)
        if self.phase==0 and i['SensorFeed']:self.phase=1
        elif self.phase==1 and i['SensorWash']:self.phase=2
        elif self.phase==2 and i['SensorWash'] and i['washComplete']:self.phase=3
        elif self.phase==3 and i['SensorWeight']:self.phase=4
        elif self.phase==4 and i['SensorWeight'] and i['weightComplete']:
            weight=real32(i['weight'])
            if 100<=weight<=200:
                self.temperature=real32(500+real32(real32(weight-100)*0.5));self.phase=6
            else:self.phase=5
        elif self.phase==5 and not i['SensorWeight']:self.phase=0
        elif self.phase==6 and i['SensorFiring']:self.phase=7
        elif self.phase==7 and i['SensorFiring'] and i['firingComplete']:self.phase=8
        elif self.phase==8 and i['SensorOutput']:self.phase=9
        elif self.phase==9 and not i['SensorOutput']:self.phase=0
        return dict(MotorForward=self.phase in (1,3,6,8),MotorReverse=False,
                    kick=self.phase==5,CompletionLight=self.phase==9,firingTemp=self.temperature)
