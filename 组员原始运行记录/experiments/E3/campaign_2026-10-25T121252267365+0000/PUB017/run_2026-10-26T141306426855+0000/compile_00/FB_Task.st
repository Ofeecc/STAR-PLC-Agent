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
 prevAdd : BOOL;
 prevDel : BOOL;
 prevMod : BOOL;
 prevQuery : BOOL;
 i : INT;
 matchIdx : INT;
 emptyIdx : INT;
 found : BOOL;
END_VAR

recipeAdded := FALSE;
recipeDeleted := FALSE;
recipeModified := FALSE;
error := FALSE;
status := 0;

IF addRecipe AND NOT prevAdd THEN
    found := FALSE;
    FOR i := 1 TO 10 DO
        IF recipe[i].recipeID = recipeIn.recipeID AND recipeIn.recipeID <> 0 THEN
            found := TRUE;
        END_IF;
    END_FOR;

    IF found THEN
        error := TRUE;
        status := 16#8002;
    ELSE
        emptyIdx := 0;
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = 0 AND emptyIdx = 0 THEN
                emptyIdx := i;
            END_IF;
        END_FOR;

        IF emptyIdx = 0 THEN
            error := TRUE;
            status := 16#8003;
        ELSE
            recipe[emptyIdx] := recipeIn;
            recipeAdded := TRUE;
        END_IF;
    END_IF;
ELSIF deleteRecipe AND NOT prevDel THEN
    matchIdx := 0;
    FOR i := 1 TO 10 DO
        IF recipe[i].recipeID = recipeIn.recipeID AND recipeIn.recipeID <> 0 THEN
            matchIdx := i;
            EXIT;
        END_IF;
    END_FOR;

    IF matchIdx = 0 THEN
        error := TRUE;
        status := 16#8004;
    ELSE
        recipe[matchIdx].recipeID := 0;
        recipeDeleted := TRUE;
    END_IF;
ELSIF modifyRecipe AND NOT prevMod THEN
    matchIdx := 0;
    FOR i := 1 TO 10 DO
        IF recipe[i].recipeID = recipeIn.recipeID AND recipeIn.recipeID <> 0 THEN
            matchIdx := i;
            EXIT;
        END_IF;
    END_FOR;

    IF matchIdx = 0 THEN
        error := TRUE;
        status := 16#8005;
    ELSE
        recipe[matchIdx] := recipeIn;
        recipeModified := TRUE;
    END_IF;
ELSIF queryRecipe AND NOT prevQuery THEN
    matchIdx := 0;
    FOR i := 1 TO 10 DO
        IF recipe[i].recipeID = recipeIn.recipeID AND recipeIn.recipeID <> 0 THEN
            matchIdx := i;
            EXIT;
        END_IF;
    END_FOR;

    IF matchIdx = 0 THEN
        error := TRUE;
        status := 16#8001;
    ELSE
        recipeQueryResult := recipe[matchIdx];
    END_IF;
END_IF;

prevAdd := addRecipe;
prevDel := deleteRecipe;
prevMod := modifyRecipe;
prevQuery := queryRecipe;
END_FUNCTION_BLOCK
