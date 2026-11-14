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
    recipeQueryResult : ST_Recipe := (recipeID := 0, ingredientType := 0, ingredientRatio := 0.0, productionTemperature := 0.0);
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    status : WORD := 16#0000;
END_VAR
VAR_IN_OUT
    recipe : ARRAY[1..10] OF ST_Recipe;
END_VAR
VAR
    prevAdd : BOOL := FALSE;
    prevDelete : BOOL := FALSE;
    prevModify : BOOL := FALSE;
    prevQuery : BOOL := FALSE;
    addEdge : BOOL;
    deleteEdge : BOOL;
    modifyEdge : BOOL;
    queryEdge : BOOL;
    invalidRequest : BOOL;
    matchIndex : INT;
    emptyIndex : INT;
    i : INT;
END_VAR

addEdge := addRecipe AND NOT prevAdd;
deleteEdge := deleteRecipe AND NOT prevDelete;
modifyEdge := modifyRecipe AND NOT prevModify;
queryEdge := queryRecipe AND NOT prevQuery;

(* Invalid calls are outside the PLC contract; a host must reject them before invocation. *)
invalidRequest := (addEdge AND (deleteEdge OR modifyEdge OR queryEdge))
    OR (deleteEdge AND (modifyEdge OR queryEdge))
    OR (modifyEdge AND queryEdge)
    OR (addEdge AND (recipeIn.recipeID = 0));

IF NOT invalidRequest THEN
    prevAdd := addRecipe;
    prevDelete := deleteRecipe;
    prevModify := modifyRecipe;
    prevQuery := queryRecipe;

    recipeAdded := FALSE;
    recipeDeleted := FALSE;
    recipeModified := FALSE;
    error := FALSE;
    status := 16#0000;

    matchIndex := 0;
    emptyIndex := 0;
    IF addEdge OR deleteEdge OR modifyEdge OR queryEdge THEN
        FOR i := 1 TO 10 DO
            IF recipe[i].recipeID = 0 THEN
                IF emptyIndex = 0 THEN
                    emptyIndex := i;
                END_IF;
            ELSIF (recipe[i].recipeID = recipeIn.recipeID) AND (matchIndex = 0) THEN
                matchIndex := i;
            END_IF;
        END_FOR;

        IF queryEdge THEN
            IF matchIndex = 0 THEN
                error := TRUE;
                status := 16#8001;
            ELSE
                recipeQueryResult := recipe[matchIndex];
            END_IF;
        ELSIF addEdge THEN
            IF matchIndex <> 0 THEN
                error := TRUE;
                status := 16#8002;
            ELSIF emptyIndex = 0 THEN
                error := TRUE;
                status := 16#8003;
            ELSE
                recipe[emptyIndex] := recipeIn;
                recipeAdded := TRUE;
            END_IF;
        ELSIF deleteEdge THEN
            IF matchIndex = 0 THEN
                error := TRUE;
                status := 16#8004;
            ELSE
                recipe[matchIndex].recipeID := 0;
                recipeDeleted := TRUE;
            END_IF;
        ELSIF modifyEdge THEN
            IF matchIndex = 0 THEN
                error := TRUE;
                status := 16#8005;
            ELSE
                recipe[matchIndex] := recipeIn;
                recipeModified := TRUE;
            END_IF;
        END_IF;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
