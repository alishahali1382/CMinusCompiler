
import enum


class SemanticRoutine(enum.Enum):
    SCOPE_ENTER = "#scope_enter"
    SCOPE_EXIT = "#scope_exit"
    
    SA_TYPE_SPECIFIER_INT = "#sa_type_specifier_int"
    SA_TYPE_SPECIFIER_VOID = "#sa_type_specifier_void"
    
    SA_BEGIN_DECLERATION = "#sa_begin_decleration"
    SA_ASSIGN_NAME = "#sa_assign_name"
    SA_DECLERATION_ROLE_FUNCTION = "#sa_decleration_role_function"
    SA_DECLERATION_ROLE_VARIABLE = "#sa_decleration_role_variable"
    SA_DECLERATION_ROLE_ARRAY = "#sa_decleration_role_array"
    SA_BEGIN_FUNCTION_STATEMENT = "#sa_begin_function_statement"
    
    PID = "#pid"
    PNUM = "#pnum"
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return rf"{self.value}"


VOID_TYPE = 0
INT_TYPE = 1
FUNC_ROLE = 1
VAR_ROLE = 2
ARRAY_ROLE = 3

class ScopeItem:
    def __init__(self, name=None, type=None, code_address=None, memory_address=None, role=None, params=None) -> None:
        self.name = name
        self.type = type
        self.code_address = code_address
        self.memory_address = memory_address
        self.role = role
        self.params = params

SP_ADDR = 0
JUMP_TO_MAIN_ADDR = 1

class CodeGen:
    def __init__(self) -> None:
        self.scope_stack = [ScopeItem("output", VOID_TYPE, None, None, FUNC_ROLE, [INT_TYPE])]
        self.PB = [None] * 10000
        self.PB[0] = ["ASSIGN", "#4", SP_ADDR, None] # set the stack pointer to 4
        self.PB_index = JUMP_TO_MAIN_ADDR + 1
        
        self.PARAM_COUNTER = 500
        
        self.SS = []

    def SS_push(self, item):
        self.SS.append(item)

    def SS_pop(self, count=1):
        self.SS = self.SS[:-count]

    def SS_top(self, idx=0):
        """return SS(top-idx)"""
        return self.SS[-1-idx]


    def get_scope_item(self, name):
        for scope_item in self.scope_stack[::-1]:
            if scope_item.name == name:
                return scope_item
        return None
    
    def getaddr(self, name):
        for scope_item in self.scope_stack[::-1]:
            if scope_item.name == name:
                return scope_item.memory_address
        return None

    def code_gen(self, semantic_routine: SemanticRoutine, *args):
        # self.__getattribute__(f"semantic_routine__{semantic_routine.name.lower()}")(*args)
        semantic_routines = {
            SemanticRoutine.SCOPE_ENTER:                    self.semantic_routine__scope_enter,
            SemanticRoutine.SCOPE_EXIT:                     self.semantic_routine__scope_exit,
            SemanticRoutine.SA_TYPE_SPECIFIER_INT:          self.semantic_routine__sa_type_specifier_int,
            SemanticRoutine.SA_TYPE_SPECIFIER_VOID:         self.semantic_routine__sa_type_specifier_void,
            SemanticRoutine.SA_BEGIN_DECLERATION:           self.semantic_routine__sa_begin_decleration,
            SemanticRoutine.SA_ASSIGN_NAME:                 self.semantic_routine__sa_assign_name,
            SemanticRoutine.SA_DECLERATION_ROLE_FUNCTION:   self.semantic_routine__sa_decleration_role_function,
            SemanticRoutine.SA_DECLERATION_ROLE_VARIABLE:   self.semantic_routine__sa_decleration_role_variable,
            SemanticRoutine.SA_DECLERATION_ROLE_ARRAY:      self.semantic_routine__sa_decleration_role_array,
            SemanticRoutine.SA_BEGIN_FUNCTION_STATEMENT:    self.semantic_routine__sa_begin_function_statement,
            SemanticRoutine.PID:                            self.semantic_routine__pid,
            SemanticRoutine.PNUM:                           self.semantic_routine__pnum,
        }
        semantic_routines[semantic_routine](*args)
        # TODO


    # *********************** semantic routine implementations ***********************

    def semantic_routine__scope_enter(self, *args):
        print("called {")
        self.scope_stack.append(None) # a mark for the end of the scope
    
    def semantic_routine__scope_exit(self, *args):
        print("called }")
        while True:
            scope_item = self.scope_stack.pop()
            if scope_item is None:
                break

    def semantic_routine__pid(self, id, *args):
        print("called pid", id)
        self.SS_push(self.getaddr(id))
        # TODO
    
    def semantic_routine__pnum(self, num, *args):
        print("called pnum", num)
        self.SS_push(f"#{num}")
        # TODO

    # decleration:
    def semantic_routine__sa_begin_decleration(self, *args):
        print("called begin_decleration")
        self.scope_stack.append(ScopeItem())
        
    def semantic_routine__sa_type_specifier_int(self, *args):
        print("called type_specifier_int")
        self.scope_stack[-1].type = INT_TYPE
    
    def semantic_routine__sa_type_specifier_void(self, *args):
        print("called type_specifier_void")
        self.scope_stack[-1].type = VOID_TYPE

    def semantic_routine__sa_assign_name(self, name, *args):
        print("called assign_name", name)
        self.scope_stack[-1].name = name

    def semantic_routine__sa_decleration_role_function(self, *args):
        print("called decleration_role_function")
        self.scope_stack[-1].role = FUNC_ROLE
        self.scope_stack[-1].params = []
        
        self.scope_stack[-1].memory_address = self.PARAM_COUNTER  # RETURN ADDRESS
        self.PARAM_COUNTER += 4
        
        # if self.scope_stack[-1].type == INT_TYPE:
        if True: # I also leave RETURN_ADDRESS for void functions to match output of testcases
            self.PARAM_COUNTER += 4 # leave space for the return value, address is FUNCTION.memory_address + 4
    
    def semantic_routine__sa_decleration_role_variable(self, *args):
        print("called decleration_role_variable")
        self.scope_stack[-1].role = VAR_ROLE

        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        if self.scope_stack[-1].type == INT_TYPE:
            self.PB[self.PB_index] = ["ASSIGN", "#0", self.PARAM_COUNTER, None]
            self.PB_index += 1
            self.PARAM_COUNTER += 4
        else:
            print("ERROR: void variable decleration")

    def semantic_routine__sa_decleration_role_array(self, *args):
        print("called decleration_role_array")
        self.scope_stack[-1].role = ARRAY_ROLE
        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        # TODO: do some stuff like array size after ]
    
    def semantic_routine__sa_begin_function_statement(self, *args):
        print("called begin_function_statement")
        self.scope_stack[-1].code_address = self.PB_index
        if  self.scope_stack[-1].name == "main":
            self.PB[JUMP_TO_MAIN_ADDR] = ["JP", self.PB_index, None, None]



    

if __name__ == '__main__':
    pass
