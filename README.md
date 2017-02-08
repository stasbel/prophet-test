# Prophet test

- [TODO](#todo)
- [How it's work](#how-its-work)
- [Examples](#examples)
- [Running](#running)
- [Docker](#docker)
- [Benchmarks](#benchmarks--tests)
- [Changes](#changes)
- [Dive into code](#dive-into-code)

## TODO

- [x] Разобраться с ошибкой запуска clang'ом c-шного кода.
Вероятней всего, ошибка связана с трюком с symlink'ами:

    ```
    In file included from square-bug.c:2:
    /usr/include/stdio.h:33:11: fatal error: 'stddef.h' file not found
    # include <stddef.h>
    ```

- [ ] Добавить autocomplete для *cmd* скрипта в docker-образе.
- [ ] Разобраться с *gmp* benchmark'ом.
- [ ] flattern docker image
- [ ] docker & root priviledge

## How it's work

### Prereq

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

5. Также перемещаем shebang на первую строчку во всех .py файлах:

    ```python
    #!/usr/bin/env python
    ```

6. Идем в */prophet-gpl/include* и собираем c помощью *make*.
Результатом должен быть файл *_prophet_profile.h*.
7. Проверьте и исправьте, если нужно строчки с 4 по 15 в *config.h* (префикс wrap_path будет свой):

    ```c
    /* the clang cmd full path */
    #define CLANG_CMD "/usr/bin/clang"
    
    /* the location of the wrapper for instrument the file */
    #define CLANG_WRAP_PATH "/home/ubuntu/prophet-gpl/wrap"
    
    /* the extra include path arguments that need to pass to clang when build AST
       tree */
    #define EXTRA_CLANG_INCLUDE_PATH ""
    
    /* the gcc cmd full path */
    #define GCC_CMD "/usr/bin/gcc"
    ```

8. Пересоберите Prophet с помощью *make*.
9. Осталось только написать пару скриптов и все правильно запустить.

### Files

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

### Commands

Какие команды запускают вычисления:
    
    prophet -feature-para feature conf
    
arg | def
------------ | -------------
prophet | исполняемый файл prophet
feature | файл с параментами из обучения (я использовал *crawler/para-all.out*)
conf | конфигурационный файл

Еще можно приписать множество всевозможных флагов, а также разделить этапы локализации ошибки,
генерации патчей, их ранжирования или вообще использовать другой алгоритм.

### Flags

все: *prophet --help*

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

## Running

Есть скрипт, чтобы быстро запустить вычисления на вашем проекте, не копаясь в *.conf* и *.revlog* файлах.
Пусть у вас есть папка с проектом *src_dir*, нужно соблюсти следующие условия:

1. Есть *Makefile* с раздельной компиляцией и линковкой.
2. Тесты лежат в *src_dir/tests*, если требуется их собрать (например, сгенерировать), то можно поставить там *Makefile*. Тесты должны быть вида *testчисло*.
3. В корневой папке *src_dir* должен лежать скрипт *run_test*, который по номеру теста выдает либо *positive* либо *negative*, в зависимости от того, правильный это тест или нет.

Тогда можно просто клонировать этот репозиторий и запустить *prophet* так:

```makefile
src/run src_dir
```

Также можно изменить пути к *prophet'у* и параметрам обучения в *src/Makefile*. Флаги *src/run*:

dep | def
------------ | -------------
-h, --help | print usage
-b, --bugged-file | если вы знаете, в каком файле ошибка, то его можно указать prophet'у (относительно *src_dir*)
-f, --full-serach | запускаем prophet с флагами -full-explore -full-synthesis -cond-ext
other | все остальные флаги передадутся prophet'у при запуске

Все результаты работы будут помещены в папку *workdir/* из папки, в которой вы запускали *src/run*.

## Docker

### Description

Есть готовый docker-образ по имени *stasbel/prophet* (https://hub.docker.com/r/stasbel/prophet/, ~8.6G). Внутри - необходимое окружение для корректной сборки и запуска *prophet'a*, а так же подготовленные 3 теста из 19 с рабочими фиксами из статьи (об этом ниже в разделе benchmarks). Собственно *prophet* уже собран и готов к запуску. Все deps'ы и файлы, необходимые для бенчмарков также собраны (их можно удалить, если не собираетесь запускать тесты и лучше не трогать, если собираетесь). Окружение, а также структура папок и файлов специально имитируют образ на *AWS*, для того чтобы все вычисления можно было проделать по инструкции с сайта *prophet* и ничего при этом не изменяя (это не совсем правда, разрабы умудрились захардкодить некоторые пути, их придется менять sed'ом). Ошибки со сборкой benchmark'ов пофикшены, правда проект *gmp* так и не удалось собрать: вылезает какая-то редкая ошибка c кодом на *c++* (что странно), поэтому *gmp* просто закомментирован в Makefile'e и вообще не собирается, все равно его вклад в результат не велик.

### Fastrun

Быстрый запуск контейнера:

```
docker pull stasbel/prophet
docker run -it -u="ubuntu" -w="/home/ubuntu/" stasbel/prophet /bin/bash -l # user=ubuntu, pass=123
```

### IDE

Если хочется работать и изменять код prophet'a в IDE, то в тупую это сделать не получится. Shared folder docker'a сильно снижает скорость (x10-20), что приводит к невозможности завершить исполнение prophet'a на больших проектах. Поэтому нужные быстрые альтернативы. Один из вариантов на MacOsX: https://github.com/brikis98/docker-osx-dev, здесь используется комбинация boot2docker + rsync, что позволяет, например, изменять код на CLion у себя, тут же видеть изменения в контейнере и там же пересобирать и тестировать. У меня, вроде, все работает ок.

### FS

Описание важных файлов и папок:

file | def
------------ | -------------
benchmarks | файлы для benchmark'ов (deps'ы для сборки и тестов)
build | тесты (примечание: сохранено авторское название)
examples | простые проекты на C, сохраненные автором для проверки работы prophet'a (spoiler: все работает)
crawler | файлы для вытаскивания параметров обучения, поиска коммитов по гитхабу
tests/tools | скрипты для benchmark'ов
wrap | обертки проффилировщика для запуска компиляции и линковки на c, c++
src | исходники на c и исполняемые файлы
cmd | мой скрипт в помощь (инфа ниже)

### Script

Написал небольшой скрипт на питоне, чтобы было удобней собирать и тестировать *prophet*.  Запуск: *cmd [arg]* (комманда - глобальная):

flg/arg | def
------------ | -------------
-h, --help | print usage
build | сборка prophet'a, при изменении одного файла - пересобирается только этот файл
check | пройти тесты от разрабов (спойлер: все ок)
test N T | протестировать prophet на N тестах, не более T часов на каждом, вывести результат и подсчитать всякие метрики
emacs-clean | удалить backup'ы emacs'a
size | узнать текущий размер контейнера
git-test-repo/git-clean | скачать/удалить этот репозиторий

### Root

Я не делаю все от рута, потому-что начнут падать некоторые тесты php. Это может помешать при запуске prophet'a на некоторых тестах, надо за этим следить.

## Benchmarks & Tests

### Description

Успешно запускается на всех benchmark'ах и проходит все тесты как надо (по крайней мере - должно = я проверил на 5-6 разных проектах и везде все ок, а чтобы проверить все мне нужно 19*12 часов). К сожалению, тесты не получится запустить в чистую по инструкции с сайта prophet'a: пути немного разные (у авторов предполагалось, что папки src и benchmarks будут дублироваться = в проектах можно было найти обе пары путей, что странно, я это исправляю sed'aми). В данный момент, на docker-образе готовы 3 теста: 2adf58c, 5a8c917 и 8ba00176 (все - php). Почему не больше: каждый весит по ~1G и больше мой макбук не выдержит. Учитывайте, что в текущей версии контейнера для всех тестов подсчитаны файлы локализации ошибок, а для того, чтобы сделать это заново, нужно удалить папку profile и profile_localization.res из рабочих папок проектов. 

### Results

Все можно самому протестировать, запустив, например, *cmd test 3 1* и подождав 3 часа. Результаты статьи подтверждаются цифра в цифру.
![prophet-res](https://github.com/StasBel/prophet-test/blob/master/doc/prophet-res.png)

Средний номер корректого патча из простанства сгенерируемых - 11 из 100. Срeдний номер корректного из "plausible" - 1 с чем-то.

### Mails to developers

Была небольшая переписка, после которой в оригинальном образе было кое-что поравлено. Тем не менее, они не особо горят помогать или что-либо изменять. То, что лежит на сайте, и то, что лежит на AWS, сильно отличаются, что немножечко мешает, но разрабам, вроде, пофиг.

## Changes

### Description

Здесь и далее будут описываться изменения оригинального кода prophet'a и новые результаты тестирования.

### Alg

Некоторое мое видение того, что и как можно изменять на каждом этапе алгоритма:

	1. На вход подается программа и набор тестов (>0 плохих и >0 хороших). Программа - это последовательность выражений. Сначала, необходимо понять, где ошибка и что изменять.
	Задача: отсортировать выражения по подозрительности в порядке убывания.
	Решение: сортировка по компаратору: чаще запускается на плохих и реже на хороших (понимаем с помощью профилировки на питоне).
	Как улучшить: да вроде никак, хотя можно проанализировать значимость выражений и, например, считать control flow (if/while/repeat) по умолчанию более подозрительным, чем, скажем, вызов функции. В самом деле, вроде как в плохих тестах мы очень часто прыгаем не в ту ветку.
	2. Итак, есть список выражения. Берем первые сколько-то (200-5000) и изменяем, генерируя пространство патчей (взято из SPR).
	Задача: сгенерировать патчи, модифицировав одно место в коде.
	Решение: взято из статьи про SPR.
	Как улучшить: хотелось бы, чтобы мы не генерировали мусора. Хорошим решением было бы поисследовать, какие изменения чаще приводят к хорошим патчам, а какие реже. Ну и, естественно, количество и качество изменений можно улучшать.
	3. ML
	Задача: (1) обучение: получаем файлы с feature векторами (2) extract program value features and modification features from each patch, then map into a binary feature vector (3) ml: каждому патчу даем score => сортируем по score, получая некоторый validation order
	Решение: хитрым образом мапаем (описано в статье, там мы учитываем MF и PVF) + ml (градиентный спуск?)
	Как улучшить:
		(1) можно улучшить часть learning: посмотреть на crawler, обходить больше проектов, получить новые файлы para.out и посмотреть на то, как они влияют на результаты
		(2) можно посмотреть, улучшаем ли идея с разными features
		(3) мне сложно сказать насчет ml
	4. Проходимся по патчам в validation order и проверяем, проходят ли они тесты. Основная часть времени работы.
	Задача: последовательность патчей и тесты, найти хорошие
	Решение: применили патч, перекомпилировали, заново проходим все тесты
	Как улучшить: казалось бы, здесь мы делаем очень много ненужной работы. Допустим у php 7000 тестов. Наврятли изменение одного выражения влияет на все 7k, но вот как это понять не совсем ясно. Скорее всего, эту часть принципиально улучшить тоже не получится.

### Changes

1. Nothing

		==============STAT==============
		test | candidates | test_eval | fixies
		php-2adf58: 60351 23228 1
		php-5a8c917: 40758 35137 1
		php-8ba00176: 89230 28201 0
		==============METRICS==============
		average number of fixies over tests: 0.666666666667

## Dive into code

### Observations

1. Инкрементальная компиляция выполняется только для php, причем она тупо захардкожена в код prophet'a.
2. 
   С локализацией ошибок все интересно: сначала мы запускаем тестирование на всех плохих тестах. Потом берем минимум и максимум из номеров плохих,
   формируя некий отрезок из номеров, которые нам интересны, а потом увеличиваем этот отрезок в обе стороны на 200. Хорошие тесты
   берем только с номерами, попавшими в новый отрезок. Зачем так сделано - не ясно.

	Далее, для каждого места в коде, мы формируем четверку (-score, beforeend\_cnt, loc, pid), где score=neg*1000000 - pos, где neg - количество запусков на плохих тестат, а pos - на хороших, beforeend\_cnt - предположительно, минимальное время в тиках до завершения работы начиная с этого выражения, loc - место в коде, включающее в себя файл и номер строки/столбца, pid - грубо говоря, номер теста на котором достигнуто минимальное beforeend_cnt. Далее мы заводим две очереди с приоритетом, в первую пихаем 4980 максимальных четверок по всем выражениям из плохих тестов, во вторую - 20 максимальных во всем выражениям из плохих, но только из bugged\_files, если указано. Далее достаем по очереди все из первой очереди, потом все из второй, проверяя что не попали в одинаковые loc'и.

	Весь этот способ вызывает сомнения: способ вычисления score, константы 4980, 20 и 1000000 надо как-то объяснять.
3. 
   Внутри prophet'a неправильно считается количество патчей (но есть скрипт, который делает это правильно, он и использовался для статьи). Дело в том, что
   некоторые partial instantained pathces могут иметь повторяющиеся abstract conditions, которые внутри представляются разные классами clang::Expr с одинаковыми
   внутренностями (поэтому prophet и не видит разницы, помещая все в set). Это легко исправляется. Скорее всего, эта ошибка идет еше с SPR.
   
   Исправил.
