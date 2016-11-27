# Prophet test

- [TODO](#todo)
- [Prereq](#prereq)
- [Files](#files)
- [Commands](#commands)
- [Flags](#flags)
- [Examples](#examples)

## TODO

- [ ] Разобраться с ошибкой запуска clang'ом c-шного кода.
Вероятней всего, ошибка связана с трюком с symlink'ами:

    ```
    In file included from square-bug.c:2:
    /usr/include/stdio.h:33:11: fatal error: 'stddef.h' file not found
    # include <stddef.h>
    ``` 

## Prereq

1. Убеждаемся, что Prophet собирается и запускается по инструкции Тимофея c почты.
2. Нам потребуется *clang-3.6*. Убеждаемся, что он есть и работает, а если нет:

    ```
    sudo apt-get install clang-3.6
    ```

3. Нам также потребуется *gcc*:

    ```
    sudo apt-get install gcc
    ```

4. Идем в */prophet-gpl/wrap* и собираем с помощью *make*.
Убеждаемся, что в папке нет файлов *gcc*, *cc* или *g++*.
Тут же в файле *pclang.py* примерно на 152 строчке (после того, как мы пытаемся получить значение из env) вставляем hardcode:

    ```python
    clang_cmd = "/usr/bin/clang-3.6"
    ```

5. Идем в */prophet-gpl/include* и собираем c помощью *make*.
Результатом должен быть файл *_prophet_profile.h*.
6. Проверьте и исправьте, если нужно строчки с 4 по 15 в *config.h* (префикс wrap_path будет свой):

    ```c
    /* the clang cmd full path */
    #define CLANG_CMD "/usr/bin/clang-3.6"
    
    /* the location of the wrapper for instrument the file */
    #define CLANG_WRAP_PATH "/home/ubuntu/prophet-gpl/wrap"
    
    /* the extra include path arguments that need to pass to clang when build AST
       tree */
    #define EXTRA_CLANG_INCLUDE_PATH ""
    
    /* the gcc cmd full path */
    #define GCC_CMD "/usr/bin/gcc"
    ```

7. Пересоберите Prophet с помощью *make*.
8. Осталось только написать пару скриптов и все правильно запустить.

## Files
Какие файлы нам понадобятся для запуска:

1. Исходники на C. Хотя бы один файл с ошибкой.
2. Тесты. Хотя бы на одном программа выдает правильный результат и хотя бы на одном неправильный.
3. \*.revlog файл, где перечислены номера правильных и неправильных тестов (пример в *mytest/square.revlog*).
4. *tester_common.py* файл, просто скопируйте его из *mytest*, там нам понадобится одна функция.
5. У вас наверняка будет *Makefile*.
!!!ВАЖНО: компиляция и линковка должны быть обязательно разделены. И лучше чтобы все это делалось gcc:

    ```makefile
    gcc -c file.c -o file.o
    gcc file.o -o file
    ```

6. \*-build.py скрипт, собирающий проект.
На выхода - результат запуска *extract_arguments* из *tester_common.py*.
Важно чтобы поддерживались следующие флаги и аргументы:
    
    ```
    *-build.py [-c] [-d file] src [out] : src, args
    ```
    flag/arg | def
    ------------ | -------------
    -c | только скомпилировать
    -d | dryrun_src, то, что нужно исключить из рассмотрения при выборе аргументов из лога компиляции
    src | собственно папка проекта, abspath
    out | скрипт парсит аргументы из лога компиляции и записывает в файл, если такой есть

7. \*-test.py скрипт, собирающий проект. На выходе - номера положительных тестов
Важно чтобы поддерживались следующие флаги и аргументы:
    
    ```
    *-test.py [-p src] src test work id+ : id*
    ```
    flag/arg | def
    ------------ | -------------
    -p | этот флаг передается когда тестируем с профайлером, фактически заменяет src
    src | src папка проекта, abspath
    test | папка с тестами, abspath
    work | рабочая папка, мною не использовалась
    id+ | список номеров тестов
    
8. \*.conf - конфигурационный файл, где указаны все пути ко всем нужным файлам,
а также название файла с ошибкой (не обязательно)

## Commands
Какие команды запускают вычисления:
    
    prophet -feature-para feature conf
    
arg | def
------------ | -------------
prophet | исполняемый файл prophet
feature | файл с параментами из обучения (я использовал *crawler/para-all.out*)
conf | конфигурационный файл

Еще можно приписать множество всевозможных флагов, а также разделить этапы локализации ошибки,
генерации патчей, их ранжирования или вообще использовать другой алгоритм.

## Flags

все: *make help*

важные:

flag | def
------------ | -------------
-consider-all | рассматриваем все файлы, а не только bugged_file из *.conf файла
-full-explore | заканчиваем вычисления только когда испробовали все в search space
-full-synthesis | перебираем все условия вместо выбора первого
-naive | запускаем наивное исправление кода, только удаляем и вставляем выражения
-random | рандомный выбор кандидатов в search space
-stats | статистика

## Examples

###1. Вычисление квадрата числа с ошибкой:
Исходник:
```c
int calc(int arg) {
    if (arg != 487) {
        return arg * arg;
    } else {
        return arg + 1;
    }
}
```
Лучший патч (из 5):
```c
int calc(int arg) {
    //prophet generated patch
    if ((arg != 487) || (1)) {
        return arg * arg;
    } else {
        return arg + 1;
    }
}
```
И статистика:
```
Total 67 different repair schemas!!!!
Total 138 different repair candidate templates for scoring!!!
Total 102 different partial repair candidate templates!!
```
[Остальные патчи и прочая инфа.](https://github.com/StasBel/prophet-test/tree/master/results/square/)
