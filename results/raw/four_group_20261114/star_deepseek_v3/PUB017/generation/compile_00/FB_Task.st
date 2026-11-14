FUNCTION_BLOCK FB_Task
VAR_INPUT
    addRecipe : BOOL;
    deleteRecipe : BOOL;
    modifyRecipe : BOOL;
    queryRecipe : BOOL;
    recipeIn : ST_Recipe;
END_VAR
VAR_OUTPUT
    recipeAdded : BOOL := FALSE;
    recipeDeleted : BOOL := FALSE;
    recipeModified : BOOL := FALSE;
    recipeQueryResult : ST_Recipe;
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    status : WORD := 0;
END_VAR
VAR_IN_OUT
    recipe : ARRAY[1..10] OF ST_Recipe;
END_VAR
VAR
    prevAddRecipe : BOOL := FALSE;
    prevDeleteRecipe : BOOL := FALSE;
    prevModifyRecipe : BOOL := FALSE;
    prevQueryRecipe : BOOL := FALSE;
    riseAdd : BOOL;
    riseDelete : BOOL;
    riseModify : BOOL;
    riseQuery : BOOL;
    riseCount : INT;
    i : INT;
    foundIndex : INT;
    found : BOOL;
    emptyIndex : INT;
    emptyFound : BOOL;
    latchedRecipeIn : ST_Recipe;
END_VAR

// default outputs for this scan
recipeAdded := FALSE;
recipeDeleted := FALSE;
recipeModified := FALSE;
error := FALSE;
status := 0;

// rising-edge detection
riseAdd := addRecipe AND NOT prevAddRecipe;
riseDelete := deleteRecipe AND NOT prevDeleteRecipe;
riseModify := modifyRecipe AND NOT prevModifyRecipe;
riseQuery := queryRecipe AND NOT prevQueryRecipe;

riseCount := 0;
IF riseAdd THEN
    riseCount := riseCount + 1;
END_IF;
IF riseDelete THEN
    riseCount := riseCount + 1;
END_IF;
IF riseModify THEN
    riseCount := riseCount + 1;
END_IF;
IF riseQuery THEN
    riseCount := riseCount + 1;
END_IF;

IF riseCount = 1 THEN
    latchedRecipeIn := recipeIn;

    IF riseAdd THEN
        IF latchedRecipeIn.recipeID <> 0 THEN
            found := FALSE;
            emptyFound := FALSE;
            emptyIndex := 0;
            FOR i := 1 TO 10 DO
                IF recipe[i].recipeID = latchedRecipeIn.recipeID THEN
                    found := TRUE;
                END_IF;
                IF (recipe[i].recipeID = 0) AND NOT emptyFound THEN
                    emptyFound := TRUE;
                    emptyIndex := i;
                END_IF;
            END_FOR;

            IF found THEN
                error := TRUE;
                status := 16#8002;
            ELSIF NOT emptyFound THEN
                error := TRUE;
                status := 16#8003;
            ELSE
                recipe[emptyIndex] := latchedRecipeIn;
                recipeAdded := TRUE;
                error := FALSE;
                status := 0;
            END_IF;
        END_IF;
    ELSIF riseDelete THEN
        found := FALSE;
        foundIndex := 0;
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = latchedRecipeIn.recipeID THEN
                found := TRUE;
                foundIndex := i;
                EXIT;
            END_IF;
        END_FOR;

        IF NOT found THEN
            error := TRUE;
            status := 16#8004;
        ELSE
            recipe[foundIndex].recipeID := 0;
            recipeDeleted := TRUE;
            error := FALSE;
            status := 0;
        END_IF;
    ELSIF riseModify THEN
        found := FALSE;
        foundIndex := 0;
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = latchedRecipeIn.recipeID THEN
                found := TRUE;
                foundIndex := i;
                EXIT;
            END_IF;
        END_FOR;

        IF NOT found THEN
            error := TRUE;
            status := 16#8005;
        ELSE
            recipe[foundIndex] := latchedRecipeIn;
            recipeModified := TRUE;
            error := FALSE;
            status := 0;
        END_IF;
    ELSIF riseQuery THEN
        found := FALSE;
        foundIndex := 0;
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = latchedRecipeIn.recipeID THEN
                found := TRUE;
                foundIndex := i;
                EXIT;
            END_IF;
        END_FOR;

        IF NOT found THEN
            error := TRUE;
            status := 16#8001;
        ELSE
            recipeQueryResult := recipe[foundIndex];
            error := FALSE;
            status := 0;
        END_IF;
    END_IF;
END_IF;

prevAddRecipe := addRecipe;
prevDeleteRecipe := deleteRecipe;
prevModifyRecipe := modifyRecipe;
prevQueryRecipe := queryRecipe;
END_FUNCTION_BLOCK
