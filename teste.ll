; ModuleID = "gencode-001"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

@"fstr_float" = internal constant [5 x i8] c"%f \0a\00"
@"fstr_int" = internal constant [5 x i8] c"%d \0a\00"
define i32 @"main"() 
{
entry:
  %"b" = alloca i32
  %"a" = alloca i32
  store i32 1, i32* %"b"
  %".3" = load i32, i32* %"b"
  %".4" = icmp eq i32 %".3", 10
  br i1 %".4", label %"entry.if", label %"entry.else"
entry.if:
  store i32 1, i32* %"a"
  br label %"entry.endif"
entry.else:
  store i32 2, i32* %"a"
  br label %"entry.endif"
entry.endif:
  %".10" = load i32, i32* %"a"
  %".11" = bitcast [5 x i8]* @"fstr_int" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 %".10")
  %".13" = bitcast [5 x i8]* @"fstr_float" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", double 0x3ff0000000000000)
  ret i32 0
}
