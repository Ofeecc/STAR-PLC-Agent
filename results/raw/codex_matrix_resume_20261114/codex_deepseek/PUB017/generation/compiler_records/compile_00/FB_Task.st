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
    prevAddRecipe : BOOL;
    prevDeleteRecipe : BOOL;
    prevModifyRecipe : BOOL;
    prevQueryRecipe : BOOL;
    i : INT;
    matchIndex : INT;
    emptyIndex : INT;
END_VAR

recipeAdded := FALSE;
recipeDeleted := FALSE;
recipeModified := FALSE;
error := FALSE;
status := 16#0000;

IF addRecipe AND NOT prevAddRecipe THEN
    matchIndex := 0;
    FOR i := 1 TO 10 DO
        IF (recipe[i].recipeID <> 0) AND (recipe[i].recipeID = recipeIn.recipeID) THEN
            matchIndex := i;
        END_IF;
    END_FOR;

    IF matchIndex <> 0 THEN
        error := TRUE;
        status := 16#8002;
    ELSE
        emptyIndex := 0;
        FOR i := 1 TO 10 DO
            IF (emptyIndex = 0) AND (recipe[i].recipeID = 0) THEN
                emptyIndex := i;
            END_IF;
        END_FOR;

        IF emptyIndex = 0 THEN
            error := TRUE;
            status := 16#8003;
        ELSE
            recipe[emptyIndex] := recipeIn;
            recipeAdded := TRUE;
        END_IF;
    END_IF;

ELSIF deleteRecipe AND NOT prevDeleteRecipe THEN
    matchIndex := 0;
    FOR i := 1 TO 10 DO
        IF (recipe[i].recipeID <> 0) AND (recipe[i].recipeID = recipeIn.recipeID) THEN
            matchIndex := i;
        END_IF;
    END_FOR;

    IF matchIndex = 0 THEN
        error := TRUE;
        status := 16#8004;
    ELSE
        recipe[matchIndex].recipeID := 0;
        recipeDeleted := TRUE;
    END_IF;

ELSIF modifyRecipe AND NOT prevModifyRecipe THEN
    matchIndex := 0;
    FOR i := 1 TO 10 DO
        IF (recipe[i].recipeID <> 0) AND (recipe[i].recipeID = recipeIn.recipeID) THEN
            matchIndex := i;
        END_IF;
    END_FOR;

    IF matchIndex = 0 THEN
        error := TRUE;
        status := 16#8005;
    ELSE
        recipe[matchIndex] := recipeIn;
        recipeModified := TRUE;
    END_IF;

ELSIF queryRecipe AND NOT prevQueryRecipe THEN
    matchIndex := 0;
    FOR i := 1 TO 10 DO
        IF (recipe[i].recipeID <> 0) AND (recipe[i].recipeID = recipeIn.recipeID) THEN
            matchIndex := i;
        END_IF;
    END_FOR;

    IF matchIndex = 0 THEN
        error := TRUE;
        status := 16#8001;
    ELSE
        recipeQueryResult := recipe[matchIndex];
    END_IF;
END_IF;

prevAddRecipe := addRecipe;
prevDeleteRecipe := deleteRecipe;
prevModifyRecipe := modifyRecipe;
prevQueryRecipe := queryRecipe;
END_FUNCTION_BLOCK
