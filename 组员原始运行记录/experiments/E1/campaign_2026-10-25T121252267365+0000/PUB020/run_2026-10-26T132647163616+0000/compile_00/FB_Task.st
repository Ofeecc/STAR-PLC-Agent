FUNCTION_BLOCK FB_Task
VAR_INPUT
  Mode : BOOL;
  ForwardButton : BOOL;
  ReverseButton : BOOL;
  SensorFeed : BOOL;
  SensorWash : BOOL;
  SensorWeight : BOOL;
  SensorFiring : BOOL;
  SensorOutput : BOOL;
  washComplete : BOOL;
  weightComplete : BOOL;
  weight : REAL;
  firingComplete : BOOL;
END_VAR
VAR_OUTPUT
  MotorForward : BOOL;
  MotorReverse : BOOL;
  kick : BOOL;
  CompletionLight : BOOL;
  firingTemp : REAL;
END_VAR
VAR
  phase : INT;
  prevMode : BOOL;
END_VAR

(* phase: 0 WAIT_FEED, 1 MOVE_TO_WASH, 2 WAIT_WASH, 3 MOVE_TO_WEIGHT, 4 WAIT_WEIGHT, 5 REJECT, 6 MOVE_TO_FIRING, 7 WAIT_FIRING, 8 MOVE_TO_OUTPUT, 9 OUTPUT_DONE *)
IF NOT Mode THEN
  (* manual mode: level control with conflict inhibition *)
  MotorForward := ForwardButton AND NOT ReverseButton;
  MotorReverse := ReverseButton AND NOT ForwardButton;
  kick := FALSE;
  CompletionLight := FALSE;
  phase := 0;
ELSE
  (* automatic mode *)
  IF NOT prevMode THEN
    phase := 0;
  END_IF

  MotorForward := FALSE;
  MotorReverse := FALSE;
  kick := (phase = 5);

  CASE phase OF
    0: (* WAIT_FEED *)
      IF SensorFeed THEN
        MotorForward := TRUE;
        phase := 1;
      END_IF

    1: (* MOVE_TO_WASH *)
      IF SensorWash THEN
        MotorForward := FALSE;
        phase := 2;
      ELSE
        MotorForward := TRUE;
      END_IF

    2: (* WAIT_WASH *)
      IF SensorWash AND washComplete THEN
        MotorForward := TRUE;
        phase := 3;
      END_IF

    3: (* MOVE_TO_WEIGHT *)
      IF SensorWeight THEN
        MotorForward := FALSE;
        phase := 4;
      ELSE
        MotorForward := TRUE;
      END_IF

    4: (* WAIT_WEIGHT *)
      IF SensorWeight AND weightComplete THEN
        IF (weight >= 100.0) AND (weight <= 200.0) THEN
          firingTemp := 500.0 + (weight - 100.0) * 0.5;
          MotorForward := TRUE;
          phase := 6;
        ELSE
          kick := TRUE;
          phase := 5;
        END_IF
      END_IF

    5: (* REJECT: hold at weighing station until product removed *)
      kick := TRUE;
      IF NOT SensorWeight THEN
        kick := FALSE;
        phase := 0;
      END_IF

    6: (* MOVE_TO_FIRING *)
      IF SensorFiring THEN
        MotorForward := FALSE;
        phase := 7;
      ELSE
        MotorForward := TRUE;
      END_IF

    7: (* WAIT_FIRING *)
      IF SensorFiring AND firingComplete THEN
        MotorForward := TRUE;
        phase := 8;
      END_IF

    8: (* MOVE_TO_OUTPUT *)
      IF SensorOutput THEN
        MotorForward := FALSE;
        CompletionLight := TRUE;
        phase := 9;
      ELSE
        MotorForward := TRUE;
      END_IF

    9: (* OUTPUT_DONE *)
      IF SensorOutput THEN
        CompletionLight := TRUE;
      ELSE
        CompletionLight := FALSE;
        phase := 0;
      END_IF
  END_CASE
END_IF

prevMode := Mode;
END_FUNCTION_BLOCK
