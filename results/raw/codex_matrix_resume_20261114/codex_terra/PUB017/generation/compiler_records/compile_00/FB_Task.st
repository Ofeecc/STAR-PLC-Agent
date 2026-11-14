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
    previousAdd : BOOL;
    previousDelete : BOOL;
    previousModify : BOOL;
    previousQuery : BOOL;
    addEdge : BOOL;
    deleteEdge : BOOL;
    modifyEdge : BOOL;
    queryEdge : BOOL;
    matchIndex : INT;
    emptyIndex : INT;
    index : INT;
END_VAR

addEdge := addRecipe AND NOT previousAdd;
deleteEdge := deleteRecipe AND NOT previousDelete;
modifyEdge := modifyRecipe AND NOT previousModify;
queryEdge := queryRecipe AND NOT previousQuery;
previousAdd := addRecipe;
previousDelete := deleteRecipe;
previousModify := modifyRecipe;
previousQuery := queryRecipe;

recipeAdded := FALSE;
recipeDeleted := FALSE;
recipeModified := FALSE;
error := FALSE;
status := 0;

matchIndex := 0;
emptyIndex := 0;
FOR index := 1 TO 10 DO
    IF recipe[index].recipeID = 0 THEN
        IF emptyIndex = 0 THEN
            emptyIndex := index;
        END_IF;
    ELSIF (recipe[index].recipeID = recipeIn.recipeID) AND (matchIndex = 0) THEN
        matchIndex := index;
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
    IF (matchIndex <> 0) OR (recipeIn.recipeID = 0) THEN
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
END_FUNCTION_BLOCK
