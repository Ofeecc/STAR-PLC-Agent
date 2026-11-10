FUNCTION_BLOCK FB_Task
VAR_INPUT
 addRecipe : BOOL;
 deleteRecipe : BOOL;
 modifyRecipe : BOOL;
 queryRecipe : BOOL;
 recipeIn : ST_Recipe;
END_VAR
VAR_OUTPUT
 recipeAdded : BOOL;
 recipeDeleted : BOOL;
 recipeModified : BOOL;
 recipeQueryResult : ST_Recipe;
 error : BOOL;
 status : WORD;
END_VAR
VAR_IN_OUT
 recipe : ARRAY[1..10] OF ST_Recipe;
END_VAR
VAR
 rtAdd : BOOL;
 rtDel : BOOL;
 rtMod : BOOL;
 rtQuery : BOOL;
 i : INT;
 foundIndex : INT;
 emptyIndex : INT;
END_VAR

// default pulse / status clearing
recipeAdded := FALSE;
recipeDeleted := FALSE;
recipeModified := FALSE;
error := FALSE;
status := 0;

// locate the record with the requested ID
foundIndex := 0;
FOR i := 1 TO 10 DO
    IF recipe[i].recipeID = recipeIn.recipeID AND recipeIn.recipeID <> 0 THEN
        foundIndex := i;
        EXIT;
    END_IF
END_FOR

// query
IF queryRecipe AND NOT rtQuery THEN
    IF foundIndex = 0 THEN
        error := TRUE;
        status := 16#8001;
    ELSE
        recipeQueryResult := recipe[foundIndex];
    END_IF
END_IF

// add
IF addRecipe AND NOT rtAdd THEN
    IF foundIndex <> 0 THEN
        error := TRUE;
        status := 16#8002;
    ELSE
        emptyIndex := 0;
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = 0 THEN
                emptyIndex := i;
                EXIT;
            END_IF
        END_FOR
        IF emptyIndex = 0 THEN
            error := TRUE;
            status := 16#8003;
        ELSE
            recipe[emptyIndex] := recipeIn;
            recipeAdded := TRUE;
        END_IF
    END_IF
END_IF

// delete
IF deleteRecipe AND NOT rtDel THEN
    IF foundIndex = 0 THEN
        error := TRUE;
        status := 16#8004;
    ELSE
        recipe[foundIndex].recipeID := 0;
        recipeDeleted := TRUE;
    END_IF
END_IF

// modify
IF modifyRecipe AND NOT rtMod THEN
    IF foundIndex = 0 THEN
        error := TRUE;
        status := 16#8005;
    ELSE
        recipe[foundIndex] := recipeIn;
        recipeModified := TRUE;
    END_IF
END_IF

// remember edge states
rtAdd := addRecipe;
rtDel := deleteRecipe;
rtMod := modifyRecipe;
rtQuery := queryRecipe;
END_FUNCTION_BLOCK
