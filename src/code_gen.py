
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
    SA_CALEE_WORKS = "#sa_calee_works"
    
    SA_BEGIN_PARAM = "#sa_begin_param"
    SA_ASSIGN_PARAM = "#sa_assign_param"
    
    SA_CHECK_BREAK_JP_SAVE = "sa_check_break_jp_save"
    
    SA_BEGIN_FUNCTION_CALL = "#sa_begin_function_call"
    SA_END_FUNCTION_CALL = "#sa_end_function_call"
    
    POP = "#pop"
    SAVE = "#save"
    LABEL = "#label"
    JPF = "#jpf"
    JPF_SAVE = "#jpf_save"
    JP = "#jp"
    SAVE_JUMP = "#save_jump"
    JUMP_FILL = "#jump_fill"
    FOR = "#for"
    
    SA_RETVIAL_AND_CALEE = "#sa_retvial_and_calee"
    SA_INDEX_ARRAY = "#sa_index_array"
    SA_INDEX_ARRAY_POP = "#sa_index_array_pop"
    
    PID = "#pid"
    PNUM = "#pnum"
    
    # algebraic:
    PUSH_PLUS = "#push_plus"
    PUSH_MINUS = "#push_minus"
    NEGATE_SS_TOP = "#negate_ss_top"
    DO_ADDOP = "#do_addop"
    PUSH_RELOP_GREATER = "#push_relop_greater"
    PUSH_RELOP_EQUAL = "#push_relop_equal"
    DO_RELOP = "#do_relop"
    PID_ASSIGN = "#pid_assign"
    DO_MULTIPLY = "#do_multiply"

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
    
    def __repr__(self) -> str:
        if self.role == VAR_ROLE:
            return f"<{self.name} {self.type} variable {self.memory_address}>"
        elif self.role == FUNC_ROLE:
            return f"<{self.name} {self.type} function {self.memory_address} {self.code_address}>"
        return "<>"

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
        self.function_call_SS = []

    def SS_push(self, item):
        self.SS.append(item)

    def SS_pop(self, count=1):
        self.SS = self.SS[:-count]

    def SS_top(self, idx=0):
        """return SS(top-idx)"""
        assert idx>=0, "SS_top only takes positive elements!"
        return self.SS[-1-idx]


    def get_scope_item(self, name):
        for scope_item in self.scope_stack[::-1]:
            if scope_item and scope_item.name == name:
                return scope_item
        return None
    
    def getaddr(self, name):
        for scope_item in self.scope_stack[::-1]:
            if scope_item and scope_item.name == name:
                return scope_item.memory_address
        return None
    
    def gettemp(self):
        self.PARAM_COUNTER += 4
        return self.PARAM_COUNTER - 4

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
            SemanticRoutine.SA_CALEE_WORKS:                 self.semantic_routine__sa_calee_works,
            SemanticRoutine.SA_BEGIN_PARAM:                 self.semantic_routine__sa_begin_param,
            SemanticRoutine.SA_ASSIGN_PARAM:                self.semantic_routine__sa_assign_param,
            SemanticRoutine.SA_CHECK_BREAK_JP_SAVE:         self.semantic_routine__check_break_jp_save,
            SemanticRoutine.SAVE:                           self.semantic_routine__save,
            SemanticRoutine.POP:                            self.semantic_routine__pop,
            SemanticRoutine.LABEL:                          self.semantic_routine__label,
            SemanticRoutine.JPF:                            self.semantic_routine__jpf,
            SemanticRoutine.JPF_SAVE:                       self.semantic_routine__jpf_save,
            SemanticRoutine.JP:                             self.semantic_routine__jp,
            SemanticRoutine.SAVE_JUMP:                      self.semantic_routine__save_jump,
            SemanticRoutine.JUMP_FILL:                      self.semantic_routine__jump_fill,
            SemanticRoutine.FOR:                            self.semantic_routine__for,
            SemanticRoutine.SA_RETVIAL_AND_CALEE:           self.semantic_routine__sa_retval_and_calee,
            SemanticRoutine.SA_INDEX_ARRAY:                 self.semantic_routine__sa_index_array,
            SemanticRoutine.SA_INDEX_ARRAY_POP:             self.semantic_routine__sa_index_array_pop,
            SemanticRoutine.PID:                            self.semantic_routine__pid,
            SemanticRoutine.PNUM:                           self.semantic_routine__pnum,
            SemanticRoutine.PUSH_PLUS:                      self.semantic_routine__push_plus,
            SemanticRoutine.PUSH_MINUS:                     self.semantic_routine__push_minus,
            SemanticRoutine.NEGATE_SS_TOP:                  self.semantic_routine__negate_ss_top,
            SemanticRoutine.DO_ADDOP:                       self.semantic_routine__do_addop,
            SemanticRoutine.PUSH_RELOP_GREATER:             self.semantic_routine__push_relop_greater,
            SemanticRoutine.PUSH_RELOP_EQUAL:               self.semantic_routine__push_relop_equal,
            SemanticRoutine.DO_RELOP:                       self.semantic_routine__do_relop,
            SemanticRoutine.PID_ASSIGN:                     self.semantic_routine__pid_assign,
            SemanticRoutine.DO_MULTIPLY:                    self.semantic_routine__do_multiply,
            SemanticRoutine.SA_BEGIN_FUNCTION_CALL:         self.semantic_routine__sa_begin_function_call,
            SemanticRoutine.SA_END_FUNCTION_CALL:           self.semantic_routine__sa_end_function_call,
        }
        semantic_routines[semantic_routine](*args)
        # print(" "*50, self.scope_stack)
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

    # function call:
    def semantic_routine__sa_begin_function_call(self, func_name, *args):
        print("called begin_function_call")
        func_scope_item = self.get_scope_item(func_name)
        if func_scope_item is None:
            print("ERROR: function not found")
            return
        if func_scope_item.role != FUNC_ROLE:
            print(f"ERROR: {func_name} is not a function")
            return
        self.function_call_SS.append(func_scope_item)
    
    def semantic_routine__sa_end_function_call(self, *args):
        print("called end_function_call")
        func_scope_item = self.function_call_SS.pop()
        if func_scope_item.name == "output":
            self.PB[self.PB_index] = ["PRINT", self.SS_top(), None, None]
            self.PB_index += 1
            self.SS_pop()
        else:
            pass
        #     self.PB[self.PB_index] = ["CALL", func_scope_item.code_address, self.SS_top(), None]
        #     self.PB_index += 1
        # self.SS_pop()
        # TODO

    # algebraic:
    def semantic_routine__push_plus(self, *args):
        print("called push_plus")
        self.SS_push("ADD")
    
    def semantic_routine__push_minus(self, *args):
        print("called push_minus")
        self.SS_push("SUB")
    
    def semantic_routine__negate_ss_top(self, *args):
        print("called negate_ss_top")
        if isinstance(self.SS_top(), str) and self.SS_top().beginwith("#"):
            self.SS[-1] = f"#{-int(self.SS_top()[1:])}"
            # TODO: remove this if it causes problems
        else:
            t = self.gettemp()
            self.PB[self.PB_index] = ["SUB", "#0", self.SS_top(), t]
            self.PB_index += 1
            self.SS_pop()
            self.SS_push(t)

    def semantic_routine__do_addop(self, *args):
        print("called do_addop")
        t = self.gettemp()
        self.PB[self.PB_index] = [self.SS_top(1), self.SS_top(2), self.SS_top(), t]
        self.PB_index += 1
        self.SS_pop(3)
        self.SS_push(t)
    
    def semantic_routine__push_relop_greater(self, *args):
        print("called push_relop_greater")
        self.SS_push("LT")
    
    def semantic_routine__push_relop_equal(self, *args):
        print("called push_relop_equal")
        self.SS_push("EQ")
    
    def semantic_routine__do_relop(self, *args):
        print("called do_relop")
        t = self.gettemp()
        self.PB[self.PB_index] = [self.SS_top(1), self.SS_top(2), self.SS_top(), t]
        self.PB_index += 1
        self.SS_pop(3)
        self.SS_push(t)
    
    def semantic_routine__pid_assign(self, *args):
        print("called pid_assign")
        print(">"*20, self.SS,)
        self.PB[self.PB_index] = ["ASSIGN", self.SS_top(), self.SS_top(1), None]
        self.PB_index += 1
        print(" "*40, self.PB[self.PB_index-1])
        self.SS_pop(1) # NOTE: only pop 1, and the result remains on top of the stack
        print(">"*20, self.SS,)

    def semantic_routine__do_multiply(self, *args):
        print("called do_multiply")
        t = self.gettemp()
        self.PB[self.PB_index] = ["MULT", self.SS_top(), self.SS_top(1), t]
        self.PB_index += 1
        self.SS_pop(2)
        self.SS_push(t)
        
    def semantic_routine__sa_calee_works(self, *args):
        #TODO
        pass

    def semantic_routine__sa_assign_param(self, *args):
        #TODO
        pass

    def semantic_routine__sa_begin_param(self, *args):
        #TODO
        pass
    
    def semantic_routine__check_break_jp_save(self, *args):
        #TODO
        pass
    
    def semantic_routine__pop(self, *args):
        self.SS_pop()
    
    def semantic_routine__save(self, *args):
        print("called save")
        print(">"*20, self.SS,)
        self.SS_push(self.PB_index)
        self.PB_index += 1
        print(">"*20, self.SS,)
        
    def semantic_routine__label(self, *args):
        print("called label")
        print(">"*20, self.SS,)
        self.SS_push(self.PB_index)
        print(">"*20, self.SS,)
    
    def semantic_routine__jpf(self, *args):
        print("called jpf")
        print(">"*20, self.SS,)
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(2)
        print(">"*20, self.SS,)
    
    def semantic_routine__jpf_save(self, *args):
        print("called jpf_save")
        print(">"*20, self.SS,)
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index + 1, None]
        self.SS_pop(2)
        self.SS_push(self.PB_index)
        self.PB_index += 1
        print(">"*20, self.SS,)
    
    def semantic_routine__jp(self, *args):
        print("called jp")
        print(">"*20, self.SS,)
        self.PB[self.SS_top()] = ["JP", self.PB_index, None, None]
        self.SS_pop(1)
        print(">"*20, self.SS,)
    
    def semantic_routine__save_jump(self, *args):
        print("called save_jump")
        print(">"*20, self.SS,)
        t = self.gettemp()
        self.PB[self.PB_index] = ["EQ", self.SS_top(), "#0", t]
        self.SS_push(self.PB_index + 2)
        self.SS_push(t)
        self.SS_push(self.PB_index + 1)
        self.PB_index += 3
        print(">"*20, self.SS,)
    
    def semantic_routine__jump_fill(self, *args):
        print("called jump_fill")
        print(">"*20, self.SS,)
        self.SS_pop()
        self.PB[self.PB_index] = ["JP", self.SS_top(4), None, None]
        self.PB_index += 1
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(2)
        print(">"*20, self.SS,)
    
    def semantic_routine__for(self, *args):
        print("called for")
        print(">"*20, self.SS,)
        #self.SS_pop()
        self.PB[self.PB_index] = ["JP", self.SS_top() + 1, None, None]
        self.PB_index += 1
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(3)
        print(">"*20, self.SS,)
    
    def semantic_routine__sa_retval_and_calee(self, *args):
        #TODO
        pass
    
    def semantic_routine__sa_index_array(self, **args):
        #TODO
        pass
    
    def semantic_routine__sa_index_array_pop(self, **args):
        #TODO
        pass

if __name__ == '__main__':
    pass
