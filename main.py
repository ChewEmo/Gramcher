import searching_blanks
import specialchinesechara
Ob=str(input('输入你需要检查的代码:'))
check_blanks = input('是否需要检查空格?是请输入1,否请输入0:')
if check_blanks == '1':
    searching_blanks.searching_blanks(Ob)
check_special = input('是否需要检查特殊字符?是请输入1,否请输入0:')
if check_special == '1':
    specialchinesechara.specialchinesechara(Ob)

