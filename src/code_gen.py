
import enum

# from termcolor import cprint

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
    SA_END_FUNCTION_STATEMENT = "#sa_end_function_statement"
    SA_PARAM_ROLE_INT = "#sa_param_role_int"
    SA_PARAM_ROLE_ARRAY = "#sa_param_role_array"
    SA_FUNCTION_RETURN_VALUE = "#sa_function_return_value"
    SA_FUNCTION_RETURN_JUMP = "#sa_function_return_jump"

    SA_CHECK_BREAK_JP_SAVE = "#sa_check_break_jp_save"

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
        self.params: list[ScopeItem] = params

    def __repr__(self) -> str:
        return f"<{self.name} {self.type} {self.role} {self.code_address} {self.memory_address}>"

SP_ADDR = 0
JUMP_TO_MAIN_ADDR = 1

class CodeGen:
    def __init__(self) -> None:
        self.scope_stack = [ScopeItem("output", VOID_TYPE, None, None, FUNC_ROLE, [INT_TYPE])]
        self.PB = [None] * 10000
        self.comment = [None] * 10000 # for debugging
        self.PB[0] = ["ASSIGN", "#4", SP_ADDR, None] # set the stack pointer to 4
        self.PB_index = JUMP_TO_MAIN_ADDR + 1

        self.PARAM_COUNTER = 500

        self.SS = []
        self.function_stack: list[ScopeItem] = []
        self.for_break_SS: list[list[int]] = []

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
        debug = False
        if debug:
            from copy import deepcopy
            checkpoint = deepcopy(self.PB)

        self.__getattribute__(f"{str(semantic_routine).replace('#', 'semantic_routine__')}")(*args)

        if debug:
            for i, item in enumerate(self.PB):
                if item != checkpoint[i]:
                    self.comment[i] = f"{semantic_routine}"

    def report_semantic_error(msg):
        print(f"Semantic Error! {msg}")

    # *********************** semantic routine implementations ***********************

    def semantic_routine__scope_enter(self, *args):
        self.scope_stack.append(None) # a mark for the end of the scope

    def semantic_routine__scope_exit(self, *args):
        while True:
            scope_item = self.scope_stack.pop()
            if scope_item is None:
                break

    def semantic_routine__pid(self, id, *args):
        self.SS_push(self.getaddr(id))

    def semantic_routine__pnum(self, num, *args):
        self.SS_push(f"#{num}")

    # decleration:
    def semantic_routine__sa_begin_decleration(self, *args):
        self.scope_stack.append(ScopeItem())

    def semantic_routine__sa_type_specifier_int(self, *args):
        self.scope_stack[-1].type = INT_TYPE

    def semantic_routine__sa_type_specifier_void(self, *args):
        self.scope_stack[-1].type = VOID_TYPE

    def semantic_routine__sa_assign_name(self, name, *args):
        self.scope_stack[-1].name = name

    def semantic_routine__sa_decleration_role_function(self, *args):
        self.scope_stack[-1].role = FUNC_ROLE
        self.scope_stack[-1].params = []

        self.scope_stack[-1].memory_address = self.PARAM_COUNTER  # RETURN JUMP ADDRESS
        self.PARAM_COUNTER += 4

        self.function_stack.append(self.scope_stack[-1])

        # if self.scope_stack[-1].type == INT_TYPE:
        if True: # leave RETURN_ADDRESS for void functions to match output of testcases
            self.PARAM_COUNTER += 4 # leave space for the return value, address is FUNCTION.memory_address + 4

    def semantic_routine__sa_decleration_role_variable(self, *args):
        self.scope_stack[-1].role = VAR_ROLE

        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        if self.scope_stack[-1].type == INT_TYPE:
            self.PB[self.PB_index] = ["ASSIGN", "#0", self.PARAM_COUNTER, None]
            self.PB_index += 1
            self.PARAM_COUNTER += 4
        else:
            print("ERROR: void variable decleration")

    def semantic_routine__sa_decleration_role_array(self, *args):
        self.scope_stack[-1].role = ARRAY_ROLE
        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        # TODO: do some stuff like array size after ]
        n = int(self.SS_top()[1:]) + 1
        self.PARAM_COUNTER += 4 * n
        self.SS_pop()
        addr = self.scope_stack[-1].memory_address
        self.PB[self.PB_index] = ["ASSIGN", f"#{addr + 4}", addr, None]
        self.PB_index += 1

    def semantic_routine__sa_param_role_int(self, *args):
        self.scope_stack[-1].role = VAR_ROLE
        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        self.PARAM_COUNTER += 4
        self.function_stack[-1].params.append(self.scope_stack[-1])

    def semantic_routine__sa_param_role_array(self, *args):
        self.scope_stack[-1].role = ARRAY_ROLE
        self.scope_stack[-1].memory_address = self.PARAM_COUNTER
        self.PARAM_COUNTER += 4
        self.function_stack[-1].params.append(self.scope_stack[-1])

    def semantic_routine__sa_begin_function_statement(self, *args):
        self.function_stack[-1].code_address = self.PB_index
        if  self.function_stack[-1].name == "main":
            self.PB[JUMP_TO_MAIN_ADDR] = ["JP", self.PB_index, None, None]

    def semantic_routine__sa_end_function_statement(self, *args):
        while self.scope_stack[-1] != self.function_stack[-1]:
            self.scope_stack.pop()
        self.function_stack.pop()

    def semantic_routine__sa_function_return_value(self, *args):
        if self.function_stack[-1].type == VOID_TYPE:
            print("ERROR: function return type not found")
            return
        self.PB[self.PB_index] = ["ASSIGN", self.SS_top(), f"{self.function_stack[-1].memory_address+4}", None]
        self.PB_index += 1
        self.SS_pop()

    def semantic_routine__sa_function_return_jump(self, *args):
        if self.function_stack[-1].name != "main":
            self.PB[self.PB_index] = ["JP", f"@{self.function_stack[-1].memory_address}", None, None]
            self.PB_index += 1

    # function call:
    def semantic_routine__sa_begin_function_call(self, func_name, *args):
        func_scope_item = self.get_scope_item(func_name)
        if func_scope_item is None:
            print("ERROR: function not found")
            return
        if func_scope_item.role != FUNC_ROLE:
            print(f"ERROR: {func_name} is not a function")
            return
        self.function_stack.append(func_scope_item)

    def semantic_routine__sa_end_function_call(self, *args):
        func_scope_item = self.function_stack.pop()
        if func_scope_item == self.scope_stack[0]: # handle shadowing the output function
        # if func_scope_item.name == "output":
            self.PB[self.PB_index] = ["PRINT", self.SS_top(), None, None]
            self.PB_index += 1
            self.SS_pop()
            return
        for param in func_scope_item.params[::-1]:
            # TODO: check SS_top() type
            if param.role == VAR_ROLE:
                self.PB[self.PB_index] = ["ASSIGN", self.SS_top(), param.memory_address, None]
                self.PB_index += 1
            elif param.role == ARRAY_ROLE:
                self.PB[self.PB_index] = ["ASSIGN", self.SS_top(), param.memory_address, None]
                self.PB_index += 1
            self.SS_pop()

        self.PB[self.PB_index] = ["ASSIGN", f"#{self.PB_index+2}", f"{func_scope_item.memory_address}", None]
        self.PB_index += 1

        self.PB[self.PB_index] = ["JP", func_scope_item.code_address, None, None]
        self.PB_index += 1

        t = self.gettemp()
        if func_scope_item.type == INT_TYPE:
            self.PB[self.PB_index] = ["ASSIGN", f"{func_scope_item.memory_address+4}", t, None]
        else:
            self.PB[self.PB_index] = ["ASSIGN", "#0", t, None]
        self.PB_index += 1
        self.SS_pop() # pop the function address
        self.SS_push(t)


    # algebraic:
    def semantic_routine__push_plus(self, *args):
        self.SS_push("ADD")

    def semantic_routine__push_minus(self, *args):
        self.SS_push("SUB")

    def semantic_routine__negate_ss_top(self, *args):
        if isinstance(self.SS_top(), str) and self.SS_top().startswith("#"):
            self.SS[-1] = f"#{-int(self.SS_top()[1:])}"
            # TODO: remove this if it causes problems
        else:
            t = self.gettemp()
            self.PB[self.PB_index] = ["SUB", "#0", self.SS_top(), t]
            self.PB_index += 1
            self.SS_pop()
            self.SS_push(t)

    def semantic_routine__do_addop(self, *args):
        t = self.gettemp()
        self.PB[self.PB_index] = [self.SS_top(1), self.SS_top(2), self.SS_top(), t]
        self.PB_index += 1
        self.SS_pop(3)
        self.SS_push(t)

    def semantic_routine__push_relop_greater(self, *args):
        self.SS_push("LT")

    def semantic_routine__push_relop_equal(self, *args):
        self.SS_push("EQ")

    def semantic_routine__do_relop(self, *args):
        t = self.gettemp()
        self.PB[self.PB_index] = [self.SS_top(1), self.SS_top(2), self.SS_top(), t]
        self.PB_index += 1
        self.SS_pop(3)
        self.SS_push(t)

    def semantic_routine__pid_assign(self, *args):
        print(">"*20, self.SS,)
        self.PB[self.PB_index] = ["ASSIGN", self.SS_top(), self.SS_top(1), None]
        self.PB_index += 1
        print(" "*40, self.PB[self.PB_index-1])
        self.SS_pop(1) # NOTE: only pop 1, and the result remains on top of the stack
        print(">"*20, self.SS,)

    def semantic_routine__do_multiply(self, *args):
        t = self.gettemp()
        self.PB[self.PB_index] = ["MULT", self.SS_top(), self.SS_top(1), t]
        self.PB_index += 1
        self.SS_pop(2)
        self.SS_push(t)

    def semantic_routine__sa_check_break_jp_save(self, *args):
        is_for = len(self.for_break_SS)
        if is_for < 1:
            #TODO semantic error
            print("semantic error: break is out of for.")
        self.for_break_SS[-1].append(self.PB_index)
        self.PB_index += 1

    def semantic_routine__pop(self, *args):
        self.SS_pop()

    def semantic_routine__save(self, *args):
        self.SS_push(self.PB_index)
        self.PB_index += 1

    def semantic_routine__label(self, *args):
        self.SS_push(self.PB_index)

    def semantic_routine__jpf(self, *args):
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(2)

    def semantic_routine__jpf_save(self, *args):
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index + 1, None]
        self.SS_pop(2)
        self.SS_push(self.PB_index)
        self.PB_index += 1

    def semantic_routine__jp(self, *args):
        self.PB[self.SS_top()] = ["JP", self.PB_index, None, None]
        self.SS_pop(1)

    def semantic_routine__save_jump(self, *args):
        t = self.gettemp()
        self.PB[self.PB_index] = ["EQ", self.SS_top(), "#0", t]
        self.SS_push(self.PB_index + 2)
        self.SS_push(t)
        self.SS_push(self.PB_index + 1)
        self.PB_index += 3

    def semantic_routine__jump_fill(self, *args):
        self.SS_pop()
        self.PB[self.PB_index] = ["JP", self.SS_top(4), None, None]
        self.PB_index += 1
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(2)
        self.for_break_SS.append([])

    def semantic_routine__for(self, *args):
        self.PB[self.PB_index] = ["JP", self.SS_top() + 1, None, None]
        self.PB_index += 1
        self.PB[self.SS_top()] = ["JPF", self.SS_top(1), self.PB_index, None]
        self.SS_pop(4)
        for p in  self.for_break_SS[-1]:
            self.PB[p] = ["JP", self.PB_index, None, None]
        self.for_break_SS = self.for_break_SS[:-1]

    
    def semantic_routine__sa_index_array_pop(self,  *args):
        t = self.gettemp()
        self.PB[self.PB_index] = ["MULT", self.SS_top(), "#4", t]
        self.PB_index += 1
        self.SS_pop()
        self.PB[self.PB_index] = ["ADD", self.SS_top(), t, t]
        self.PB_index += 1
        self.SS_pop()
        self.SS_push("@" + str(t))

