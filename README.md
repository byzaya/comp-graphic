# Компьютерная графика 
(Вариант 17)

## Лабораторная работа №1

1. Изобразить каркасный конус высотой 150, основание - окружность с радиусом 100 и центром в точке O (10,10), и каркасную сферу радиусом 50 и центром в вершине конуса.
2. Выполнить поворот конуса на ⍺=-180° вокруг оси Z относительно начала координат, затем поворот сферы на ⍺=45° вокруг оси Х относительно начала координат.
3. Изобразить куб и сферу. Одна вершина куба совпадает с центром сферы. Размеры примитивов задать самостоятельно.
4. Переместить сферу так, чтобы она был расположена на кубе

## Лабораторная работа №2

Требуется разработать программу, которая создает визуализацию заданного набора трех 3D объектов. Каждый объект имеет уникальные свойства материала, и сцена освещается с использованием параметров источника света.

### Основные требования
1. **Базовые 3D объекты:** В качестве базовых объектов используются 3D примитивы, указанные в варианте задания №1.

2. **Свойства материала:**
   - Один из объектов должен иметь свойства прозрачности, где значение параметра должно быть больше 0,5.
   - Другой выбранный объект должен имитировать отполированную поверхность (shininess) с максимальным значением. Для этого следует выбирать примитивы с выпуклыми поверхностями, такие как цилиндр, тор, конус, сфера или чайник.
   - Третий объект должен иметь диффузно-рассеивающую, матовую поверхность.

3. **Источник освещения:** В сцене обязательно должен присутствовать как минимум один источник освещения. Пользователь должен иметь возможность менять параметры источника света, такие как местоположение, интенсивность и цвет освещения.

4. **Текстурирование:** Окончательный этап включает текстурирование одного из матовых объектов. Возможно также использовать микроискажение нормалей при помощи bump-mapping.

## Лабораторная работа №3

Требуется при помощи стандартных функций графической библиотеки
(OpenGL/Vulkan/DirectX) изобразить указанные объекты, затем рассчитать и
визуализировать передвижение объекта, имитирующее реальное. При этом алгоритм
перемещений должен быть рассчитан таким образом, чтобы соблюдались следующие
параметры: движущийся объект должен казаться наблюдателю тяжелым; все
объекты должны быть твердыми, т.е. «протыкать» или «проваливаться» друг в друга
они не должны. Объекты должны быть текстурированы и освещены источником
света.

1. Изобразить текстурированные цилиндр и расположенный на его основании додекаэдр.
2. Реализовать освещение (один источник).
3. Рассчитать и изобразить перекатывание додекаэдра по основанию цилиндра.

## Курсовая работа 

### Описание общей части задания.
1. В качестве источников-генераторов (еmitters) частиц выступают объекты различной конфигурации. Количество частиц в сцене варьируется от 100 до 1000. Координаты начальной позиции частицы рассчитываются при помощи случайного числа, переведенного на поверхность требуемой фигуры. Направление движения частицы определяется по нормали к поверхности фигуры, например:

Cylinder: 

      r*cos(a)

      r*sin(a)

Sphere: 

      r*cos(a)*sin(b) 

      r*sin(a)*sin(b) 

      r*sin(b)

Cone: 

      r(h)*cos(a) 

      r(h)*sin(a)

2. Каждая частица должна характеризоваться следующим набором свойств: координаты, скорость, размер, цвет (с возможным добавлением текстуры и/или прозрачности), время жизни, наличие/отсутствие следа от частицы. Свойства могут зависеть друг от друга (например, цвет частицы изменяется в зависимости от времени жизни). По окончании времени жизни частица исчезает и порождается новая частица. Тем самым система становится цикличной.


3. Так как время системы дискретно, то определяются правила поведения частиц на каждом такте (dtime). Частицы должны изменять свое расположение по определенным законам, одинаковым для всей системы. Новая позиция частицы рассчитывается по следующим правилам (в векторной форме):


      Скорость = Скорость + Ускорение * dtime; 

      Позиция = Позиция + Скорость * dtime;

Возможно использование собственных идей для расчета новой позиции частицы. Поощряется красивая формула для расчета изменений.

4. За каждой из частиц остается след, который изображается при помощи повторения частицы (поощряются также другие способы изображения следа). След может иметь различную протяженность или отсутствовать.


5. Требуется осуществить моделирование физического взаимодействия частиц с объектами в сцене. Такие взаимодействия в задании предусмотрены трех типов.
Столкновение: в качестве объектов, с которыми могут сталкиваться частицы (коллайдеров), выступают стандартные примитивы (цилиндр, сфера, куб, ограниченная плоскость). Столкновение моделируется как изменение направления движения частицы (например, на противоположное или на какое-либо единое для всех частиц) с сохранением или потерей/увеличением скорости.
Притяжение: используются «магниты»-притягиватели (аттракторы) в форме стандартных примитивов (цилиндр, ограниченная плоскость, точка). При приближении к таким объектам частицы должны изменять скорость и направление движения (по нормали к объекту) в зависимости от расстояния до него. Когда расстояние до аттрактора становится меньше заданного, частица изменяет направление движения и притягивается к аттрактору по нормали с нарастающей скоростью.
Отталкивание: используются «магниты»-отталкиватели (анти-аттракторы) также в форме стандартных примитивов (цилиндр, ограниченная плоскость, точка) Когда расстояние до анти-аттрактора становится меньше заданного, частица замедляется и затем плавно изменяет направление движения, отклоняясь от прежней траектории таким образом, чтобы удалиться от анти-аттрактора по нормали с нарастающей скоростью.

Задания предусматривают некоторую обязательную часть, отступать от которой нельзя. В остальном предполагается свобода в установлении конкретных параметров или формул изменения параметров. Можно добавлять дополнительные силы – гравитацию, ветер, точки-ускорители и т.п.; можно использовать динамически меняющиеся текстуры для отображения позиции частиц, и так далее...


### Задание 17.
1. Эмиттер – плоскость
2. Обязательные параметры: яркость частиц увеличивается по мере удаления от
эмиттера
Остальные параметры устанавливаются и изменяются по вашему выбору.
3. След: присутствует, длина от 2 до 4
4. Столкновения: конус