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

1. Изобразить текстурированные цилиндр и расположенный на его основании додекаэдр.
2. Реализовать освещение (один источник).
3. Рассчитать и изобразить перекатывание додекаэдра по основанию цилиндра.