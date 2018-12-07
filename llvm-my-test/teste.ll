; ModuleID = "gencode-001"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

define i32 @"main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"fstr" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 0)
  ret i32 0
}

@"fstr" = internal constant [5 x i8] c"%f \0a\00"
