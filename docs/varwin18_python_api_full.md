
########## _generated_ARMarker_ARMarkerWrapper.html.md
Title: ARMarkerWrapper — документация Varwin 18

_class_ ARMarker.ARMarkerWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

IsFound()→bool[]
Обнаружена

**Пример:**

value = instance.IsFound()

AddTargetFoundHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
При обнаружении метки

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnTargetFound(sender):
  pass
instance.AddTargetFoundHandler(OnTargetFound)

AddTargetLostHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
При потери метки

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnTargetLost(sender):
  pass
instance.AddTargetLostHandler(OnTargetLost)

########## _generated_BallsBox_BallsBoxWrapper.html.md

# BallsBoxWrapper[]

_class_ BallsBox.BallsBoxWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_Basketball_BasketballWrapper.html.md

# BasketballWrapper[]

_class_ Basketball.BasketballWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_Basketball_Hoop_Basketball_HoopWrapper.html.md

# Basketball_HoopWrapper[]

_class_ Basketball_Hoop.Basketball_HoopWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

AddRingHitHandler(_handler:Callable[[List[[Object]],[Object]],CoroutineType]_)→None[]
Попадание в кольцо

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   wrappers (List[Object]): wrappers

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnRingHit(wrappers, sender):
  pass
instance.AddRingHitHandler(OnRingHit)

########## _generated_BoxCollider_BoxColliderWrapper.html.md

# BoxColliderWrapper[]

_class_ BoxCollider.BoxColliderWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_CapsuleCollider_CapsuleColliderWrapper.html.md

# CapsuleColliderWrapper[]

_class_ CapsuleCollider.CapsuleColliderWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_CustomZone_CustomZoneWrapper.html.md
Title: CustomZoneWrapper — документация Varwin 18

_class_ CustomZone.CustomZoneWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

IsContainObject(_obj:[Object]_)→bool[]
Содержит [obj] в данный момент

Параметры:
**(****Object****)** (_obj_) – объект сцены

**Пример:**

value = instance.IsContainObject(sceneObject)

GetContainedObjects()→List[[Object]][]
Объекты, находящиеся внутри

**Пример:**

value = instance.GetContainedObjects()

AddObjectEnteredHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Объект попал внутрь зоны

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   zoneTarget (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnObjectEntered(zoneTarget, sender):
  pass
instance.AddObjectEnteredHandler(OnObjectEntered)

AddObjectExitedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Объект вышел наружу из зоны

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   zoneTarget (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnObjectExited(zoneTarget, sender):
  pass
instance.AddObjectExitedHandler(OnObjectExited)

########## _generated_DefaultSpawnPoint_DefaultSpawnPointWrapper.html.md

# DefaultSpawnPointWrapper[]

_class_ DefaultSpawnPoint.DefaultSpawnPointWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_Player_PlayerWrapper.html.md
Title: PlayerWrapper — документация Varwin 18

[Varwin]_class_ Player.PlayerWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ MovementType[]

Locomotion _:Any_ _=Ellipsis_[]
Движение

Teleport _:Any_ _=Ellipsis_[]
Телепортацию

All _:Any_ _=Ellipsis_[]
Любое перемещение

_class_ RotationTypes[]

ToObject _:Any_ _=Ellipsis_[]
К объекту

SameAsObject _:Any_ _=Ellipsis_[]
Так же, как

_class_ Gravity[]

GravityOn _:Any_ _=Ellipsis_[]
Подчиняется гравитации

GravityOff _:Any_ _=Ellipsis_[]
Не подчиняется гравитации

_class_ SwitchStateTypes[]

Enabled _:Any_ _=Ellipsis_[]
Включено

Disabled _:Any_ _=Ellipsis_[]
Выключено

_class_ AllowedStates[]

Allowed _:Any_ _=Ellipsis_[]
Разрешено

Prohibited _:Any_ _=Ellipsis_[]
Запрещено

_class_ VibrationPreset[]

Weak _:Any_ _=Ellipsis_[]
Слабо

Strong _:Any_ _=Ellipsis_[]
Сильно

_class_ PlayerHand[]

RightHand _:Any_ _=Ellipsis_[]
Правая рука

LeftHand _:Any_ _=Ellipsis_[]
Левая рука

BothHands _:Any_ _=Ellipsis_[]
Обе руки

_property_ WalkingSpeed _:float_[]
Cкорость ходьбы в режиме просмотра на ПК [value] м/с

**Пример:**

value = instance.WalkingSpeed

_property_ SprintSpeed _:float_[]
Скорость бега [value] м/с

**Пример:**

value = instance.SprintSpeed

_property_ JumpHeight _:float_[]
Высота прыжка [value] м

**Пример:**

value = instance.JumpHeight

_property_ PlayerNormalHeight _:float_[]
Высота игрока в режиме просмотра на ПК [value] м

**Пример:**

value = instance.PlayerNormalHeight

_property_ UseGravity _:Any_[]
Физическое свойство

Результат:
значение из перечня:

*   PlayerWrapper.Gravity.GravityOn

*   PlayerWrapper.Gravity.GravityOff

**Пример:**

value = instance.UseGravity

_property_ IsArcIsHiddenOnDisabledTeleport _:bool_[]
Скрывать луч при отключённом телепорте

**Пример:**

value = instance.IsArcIsHiddenOnDisabledTeleport

_property_ CursorIsVisible _:Any_[]
Отображение курсора в режиме Desktop

Результат:
значение из перечня:

*   PlayerWrapper.SwitchStateTypes.Enabled

*   PlayerWrapper.SwitchStateTypes.Disabled

**Пример:**

value = instance.CursorIsVisible

_property_ IsMouseLookEnabled _:Any_[]
Поворот камеры с помощью мыши в режиме Desktop

Результат:
значение из перечня:

*   PlayerWrapper.AllowedStates.Allowed

*   PlayerWrapper.AllowedStates.Prohibited

**Пример:**

value = instance.IsMouseLookEnabled

_property_ IsTurnInVREnabled _:Any_[]
Поворот в VR с помощью контроллера

Результат:
значение из перечня:

*   PlayerWrapper.AllowedStates.Allowed

*   PlayerWrapper.AllowedStates.Prohibited

**Пример:**

value = instance.IsTurnInVREnabled

_property_ ObjectInteraction _:Any_[]
Взаимодействие с объектами

Результат:
значение из перечня:

*   PlayerWrapper.AllowedStates.Allowed

*   PlayerWrapper.AllowedStates.Prohibited

**Пример:**

value = instance.ObjectInteraction

_property_ HeadPosition _:[Vector3]_[]
Положение головы

**Пример:**

value = instance.HeadPosition

_property_ HeadRotation _:[Vector3]_[]
Вращение головы

**Пример:**

value = instance.HeadRotation

_property_ PointerLength _:float_[]
Длина луча указки

**Пример:**

value = instance.PointerLength

_property_ AlwaysDrawRay _:bool_[]
Постоянно отображать луч указателя

**Пример:**

value = instance.AlwaysDrawRay

_property_ BeginWidth _:float_[]
Начальная ширина луча указки [value] м

**Пример:**

value = instance.BeginWidth

_property_ EndWidth _:float_[]
Конечная ширина луча указки [value] м

**Пример:**

value = instance.EndWidth

_property_ BeginColor _:[Color]_[]
Начальный цвет луча указки [value]

**Пример:**

value = instance.BeginColor

_property_ EndColor _:[Color]_[]
Конечный цвет луча указки [value]

**Пример:**

value = instance.EndColor

_property_ HandsRadius _:float_[]
Радиус коллайдера рук

**Пример:**

value = instance.HandsRadius

CheckHoldAnyObject()→bool[]
Держит в руках какой-нибудь объект

**Пример:**

value = instance.CheckHoldAnyObject()

CheckObjectInAnyHand(_otherObject:[Object]_)→bool[]
Держит в какой-либо из рук

Параметры:
**(****Object****)** (_otherObject_) – объект сцены

**Пример:**

value = instance.CheckObjectInAnyHand(sceneObject)

CheckObjectInLeftHand(_otherObject:[Object]_)→bool[]
Держит в левой руке

Параметры:
**(****Object****)** (_otherObject_) – объект сцены

**Пример:**

value = instance.CheckObjectInLeftHand(sceneObject)

CheckObjectInRightHand(_otherObject:[Object]_)→bool[]
Держит в правой руке

Параметры:
**(****Object****)** (_otherObject_) – объект сцены

**Пример:**

value = instance.CheckObjectInRightHand(sceneObject)

AllowMovementEverywhere()→None[]
Может двигаться везде

**Пример:**

instance.AllowMovementEverywhere()

AllowMovementOnlyTeleportArea()→None[]
Может двигаться по области перемещения

**Пример:**

instance.AllowMovementOnlyTeleportArea()

AllowMovementType(_type:int_)→None[]
Разрешить

Параметры:
**(****int****)** (_type_) –

значение из перечня:

*   PlayerWrapper.MovementType.Locomotion

*   PlayerWrapper.MovementType.Teleport

*   PlayerWrapper.MovementType.All

**Пример:**

instance.AllowMovementType(PlayerWrapper.MovementType.Locomotion)

ProhibitMovementType(_type:int_)→None[]
Запретить

Параметры:
**(****int****)** (_type_) –

значение из перечня:

*   PlayerWrapper.MovementType.Locomotion

*   PlayerWrapper.MovementType.Teleport

*   PlayerWrapper.MovementType.All

**Пример:**

instance.ProhibitMovementType(PlayerWrapper.MovementType.Locomotion)

TeleportToStartPosition()→None[]
Вернуть в начальную позицию

**Пример:**

instance.TeleportToStartPosition()

TeleportToObject(_targetObj:[Object]_)→None[]
Телепортироваться к объекту

Параметры:
**(****Object****)** (_targetObj_) – объект сцены

**Пример:**

instance.TeleportToObject(sceneObject)

TeleportToVector(_targetVector:[Vector3]_)→None[]
Телепортироваться к координатам

**Пример:**

instance.TeleportToVector(Varwin.Vector3(1,1,1))

_async_ MoveToPointWithSpeed(_target:[Vector3]_, _speed:float_)→None[]
Перемещаться к координатам [target] со скоростью [speed] м/с

**Пример:**

await instance.MoveToPointWithSpeed(Varwin.Vector3(1,1,1), 0)

_async_ MoveToObjectWithSpeed(_targetWrapper:[Object]_, _speed:float_)→None[]
Перемещаться к объекту [targetWrapper] со скоростью [speed] м/с

Параметры:
**(****Object****)** (_targetWrapper_) – объект сцены

**Пример:**

await instance.MoveToObjectWithSpeed(sceneObject, 0)

RotateHorizontally(_angle:float_)→None[]
Мгновенно повернуться в горизонтальной плоскости на [angle] градусов

**Пример:**

instance.RotateHorizontally(0)

RotateTo(_rotationTapes:int_, _target:[Object]_)→None[]
Мгновенно повернуться

Параметры:
*   **(****int****)** (_rotationTapes_) –

значение из перечня:

    *   PlayerWrapper.RotationTypes.ToObject

    *   PlayerWrapper.RotationTypes.SameAsObject

*   **(****Object****)** (_target_) – объект сцены

**Пример:**

instance.RotateTo(PlayerWrapper.RotationTypes.ToObject, sceneObject)

SetEulerAngles(_targetAngle:[Vector3]_)→None[]
Задать поворот

**Пример:**

instance.SetEulerAngles(Varwin.Vector3(1,1,1))

ForceGrabObjectInLeftHand(_otherObject:[Object]_)→None[]
Принудительно взять в левую руку

Параметры:
**(****Object****)** (_otherObject_) – объект сцены

**Пример:**

instance.ForceGrabObjectInLeftHand(sceneObject)

ForceGrabObjectInRightHand(_otherObject:[Object]_)→None[]
Принудительно взять в правую руку

Параметры:
**(****Object****)** (_otherObject_) – объект сцены

**Пример:**

instance.ForceGrabObjectInRightHand(sceneObject)

_async_ ForceDropFromBothHands()→None[]
Принудительно выпустить объекты из обеих рук

**Пример:**

await instance.ForceDropFromBothHands()

_async_ ForceDropObjectInLeftHand()→None[]
Принудительно выпустить объект из левой руки

**Пример:**

await instance.ForceDropObjectInLeftHand()

_async_ ForceDropObjectInRightHand()→None[]
Принудительно выпустить объект из правой руки

**Пример:**

await instance.ForceDropObjectInRightHand()

VibrateLeftHand(_strength:float_, _duration:float_)→None[]
Завибрировать с настройками для левой руки с силой [0..1] [strength] продолжительностью [duration] с.

**Пример:**

instance.VibrateLeftHand(0, 0)

VibrateRightHand(_strength:float_, _duration:float_)→None[]
Завибрировать с настройками для правой руки с силой [0..1] [strength] продолжительностью [duration] с.

**Пример:**

instance.VibrateRightHand(0, 0)

VibrateLeftHandPreset(_vibrationPreset:int_)→None[]
Завибрировать для левой руки с интенсивностью [vibrationPreset]

Параметры:
**(****int****)** (_vibrationPreset_) –

значение из перечня:

*   PlayerWrapper.VibrationPreset.Weak

*   PlayerWrapper.VibrationPreset.Strong

**Пример:**

instance.VibrateLeftHandPreset(PlayerWrapper.VibrationPreset.Weak)

VibrateRightHandPreset(_vibrationPreset:int_)→None[]
Завибрировать для правой руки с интенсивностью [vibrationPreset]

Параметры:
**(****int****)** (_vibrationPreset_) –

значение из перечня:

*   PlayerWrapper.VibrationPreset.Weak

*   PlayerWrapper.VibrationPreset.Strong

**Пример:**

instance.VibrateRightHandPreset(PlayerWrapper.VibrationPreset.Weak)

_async_ VibrateWithIntervals(_hand:int_, _strength:float_, _duration:float_, _interval:float_, _vibrationCount:int_)→None[]
Завибрировать для [hand] с силой [0..1] [strength] продолжительностью вибрации [duration] с. интервалом [interval] с. количеством вибраций [vibrationCount]

Параметры:
**(****int****)** (_hand_) –

значение из перечня:

*   PlayerWrapper.PlayerHand.RightHand

*   PlayerWrapper.PlayerHand.LeftHand

*   PlayerWrapper.PlayerHand.BothHands

**Пример:**

await instance.VibrateWithIntervals(PlayerWrapper.PlayerHand.RightHand, 0, 0, 0, 0)

AttachCameraToObject(_target:[Object]_, _positionOffset:[Vector3]_, _rotationOffset:[Vector3]_)→None[]
Закрепить камеру за объектом [target] со смещением позиции [positionOffset] поворота [rotationOffset]

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

instance.AttachCameraToObject(sceneObject, Varwin.Vector3(1,1,1), Varwin.Vector3(1,1,1))

DetachCameraFromObject()→None[]
Открепить камеру от объекта

**Пример:**

instance.DetachCameraFromObject()

AddAnyHandCollidedHandler(_handler:Callable[[Any,[Object],[Object]],CoroutineType]_)→None[]
Рука столкнулась [hand] с объектом [wrapperObject]

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (Any): hand

*   wrapperObject (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnAnyHandCollided(hand, wrapperObject, sender):
  pass
instance.AddAnyHandCollidedHandler(OnAnyHandCollided)

AddControllerEnabledHandler(_handler:Callable[[Any,[Object]],CoroutineType]_)→None[]
Контроллер включен

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (Any): hand

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnControllerEnabled(hand, sender):
  pass
instance.AddControllerEnabledHandler(OnControllerEnabled)

AddControllerDisabledHandler(_handler:Callable[[Any,[Object]],CoroutineType]_)→None[]
Контроллер выключен

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (Any): hand

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnControllerDisabled(hand, sender):
  pass
instance.AddControllerDisabledHandler(OnControllerDisabled)

########## _generated_SKCoin_SKCoinWrapper.html.md

# SKCoinWrapper[]

_class_ SKCoin.SKCoinWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_SKFlyingDrone_SKFlyingDroneWrapper.html.md

# SKFlyingDroneWrapper[]

_class_ SKFlyingDrone.SKFlyingDroneWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ RightLeft _:float_[]
Движение вправо-влево

**Пример:**

value = instance.RightLeft

_property_ ForwardBackward _:float_[]
Движение вперед-назад

**Пример:**

value = instance.ForwardBackward

_property_ UpDown _:float_[]
Движение вверх-вниз

**Пример:**

value = instance.UpDown

_property_ Rotation _:float_[]
Вращение

**Пример:**

value = instance.Rotation

_property_ MovementSpeed _:float_[]
Скорость передвижения

**Пример:**

value = instance.MovementSpeed

_property_ RotationSpeed _:float_[]
Скорость поворота

**Пример:**

value = instance.RotationSpeed

########## _generated_SKHumanoidBot_SKHumanoidBotWrapper.html.md

# SKHumanoidBotWrapper[]

_class_ SKHumanoidBot.SKHumanoidBotWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ Forward _:float_[]
Движение вперед

**Пример:**

value = instance.Forward

_property_ Rotation _:float_[]
Поворот

**Пример:**

value = instance.Rotation

Jump()→None[]
Прыжок

**Пример:**

instance.Jump()

########## _generated_SKJoystick_SKJoystickWrapper.html.md
Title: SKJoystickWrapper — документация Varwin 18

[Varwin]_class_ SKJoystick.SKJoystickWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ AxisX _:float_[]
Значение джойстика по горизонтальной оси

**Пример:**

value = instance.AxisX

_property_ AxisY _:float_[]
Значение джойстика по вертикальной оси

**Пример:**

value = instance.AxisY

RedButtonPressed()→bool[]
Красная кнопка нажата

**Пример:**

value = instance.RedButtonPressed()

GreenButtonPressed()→bool[]
Зеленая кнопка нажата

**Пример:**

value = instance.GreenButtonPressed()

BlueButtonPressed()→bool[]
Синяя кнопка нажата

**Пример:**

value = instance.BlueButtonPressed()

YellowButtonPressed()→bool[]
Желтая кнопка нажата

**Пример:**

value = instance.YellowButtonPressed()

AddRedButtonWasPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Красная кнопка нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnRedButtonWasPressed(sender):
  pass
instance.AddRedButtonWasPressedHandler(OnRedButtonWasPressed)

AddGreenButtonWasPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Зеленая кнопка нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnGreenButtonWasPressed(sender):
  pass
instance.AddGreenButtonWasPressedHandler(OnGreenButtonWasPressed)

AddBlueButtonWasPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Синяя кнопка нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBlueButtonWasPressed(sender):
  pass
instance.AddBlueButtonWasPressedHandler(OnBlueButtonWasPressed)

AddYellowButtonWasPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Желтая кнопка нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnYellowButtonWasPressed(sender):
  pass
instance.AddYellowButtonWasPressedHandler(OnYellowButtonWasPressed)

AddRedButtonWasReleasedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Красная кнопка отпущена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnRedButtonWasReleased(sender):
  pass
instance.AddRedButtonWasReleasedHandler(OnRedButtonWasReleased)

AddGreenButtonWasReleasedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Зеленая кнопка отпущена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnGreenButtonWasReleased(sender):
  pass
instance.AddGreenButtonWasReleasedHandler(OnGreenButtonWasReleased)

AddBlueButtonWasReleasedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Синяя кнопка отпущена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBlueButtonWasReleased(sender):
  pass
instance.AddBlueButtonWasReleasedHandler(OnBlueButtonWasReleased)

AddYellowButtonWasReleasedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Желтая кнопка отпущена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnYellowButtonWasReleased(sender):
  pass
instance.AddYellowButtonWasReleasedHandler(OnYellowButtonWasReleased)

########## _generated_SKLadder_SKLadderWrapper.html.md

# SKLadderWrapper[]

_class_ SKLadder.SKLadderWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_SKSimpleBot_SKSimpleBotWrapper.html.md

# SKSimpleBotWrapper[]

_class_ SKSimpleBot.SKSimpleBotWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ Rotation _:float_[]
Поворот

**Пример:**

value = instance.Rotation

_property_ Forward _:float_[]
Движение вперед

**Пример:**

value = instance.Forward

_property_ MovementSpeed _:float_[]
Скорость передвижения

**Пример:**

value = instance.MovementSpeed

_property_ RotationSpeed _:float_[]
Скорость поворота

**Пример:**

value = instance.RotationSpeed

ShortCircuit()→None[]
Короткое замыкание

**Пример:**

instance.ShortCircuit()

########## _generated_SphereCollider_SphereColliderWrapper.html.md

# SphereColliderWrapper[]

_class_ SphereCollider.SphereColliderWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_StreamingVarwinVideo180_StreamingVarwinVideo180Wrapper.html.md
Title: StreamingVarwinVideo180Wrapper — документация Varwin 18

_class_ StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   StreamingVarwinVideo180Wrapper.PlayerLockOptions.Lock

*   StreamingVarwinVideo180Wrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения (0..10)

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость (0..1)

**Пример:**

value = instance.Volume

_property_ Loop _:bool_[]
Зациклить

**Пример:**

value = instance.Loop

_property_ PlayOnAwake _:bool_[]
Воспроизвести на старте

**Пример:**

value = instance.PlayOnAwake

_property_ Length _:Any_[]
Длительность видео (в секундах)

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время (в секундах)

**Пример:**

value = instance.CurrentTime

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

Play()→None[]
Воспроизвести

**Пример:**

instance.Play()

LoadVideo()→None[]
Загрузить

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить

**Пример:**

instance.UnloadVideo()

Stop()→None[]
Остановить

**Пример:**

instance.Stop()

Pause()→None[]
Пауза

**Пример:**

instance.Pause()

ResetSpeed()→None[]
Восстановить исходную скорость воспроизведения

**Пример:**

instance.ResetSpeed()

Seek(_position:Any_)→None[]
Перемотать на секунду

**Пример:**

instance.Seek(0)

MuteAudio()→None[]
Выключить звук

**Пример:**

instance.MuteAudio()

UnmuteAudio()→None[]
Включить звук

**Пример:**

instance.UnmuteAudio()

AddPlaybackCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение окончено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPlaybackCompleted(sender):
  pass
instance.AddPlaybackCompletedHandler(OnPlaybackCompleted)

AddVideoLoadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Загружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnVideoLoaded(sender):
  pass
instance.AddVideoLoadedHandler(OnVideoLoaded)

########## _generated_StreamingVarwinVideo360_StreamingVarwinVideo360Wrapper.html.md
Title: StreamingVarwinVideo360Wrapper — документация Varwin 18

_class_ StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   StreamingVarwinVideo360Wrapper.PlayerLockOptions.Lock

*   StreamingVarwinVideo360Wrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения (0..10)

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость (0..1)

**Пример:**

value = instance.Volume

_property_ Loop _:bool_[]
Зациклить

**Пример:**

value = instance.Loop

_property_ PlayOnAwake _:bool_[]
Воспроизвести на старте

**Пример:**

value = instance.PlayOnAwake

_property_ Length _:Any_[]
Длительность видео (в секундах)

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время (в секундах)

**Пример:**

value = instance.CurrentTime

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

Play()→None[]
Воспроизвести

**Пример:**

instance.Play()

LoadVideo()→None[]
Загрузить

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить

**Пример:**

instance.UnloadVideo()

Stop()→None[]
Остановить

**Пример:**

instance.Stop()

Pause()→None[]
Пауза

**Пример:**

instance.Pause()

ResetSpeed()→None[]
Восстановить исходную скорость воспроизведения

**Пример:**

instance.ResetSpeed()

Seek(_position:Any_)→None[]
Перемотать на секунду

**Пример:**

instance.Seek(0)

MuteAudio()→None[]
Выключить звук

**Пример:**

instance.MuteAudio()

UnmuteAudio()→None[]
Включить звук

**Пример:**

instance.UnmuteAudio()

AddPlaybackCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение окончено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPlaybackCompleted(sender):
  pass
instance.AddPlaybackCompletedHandler(OnPlaybackCompleted)

AddVideoLoadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Загружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnVideoLoaded(sender):
  pass
instance.AddVideoLoadedHandler(OnVideoLoaded)

########## _generated_StreamingVarwinVideo_StreamingVarwinVideoWrapper.html.md
Title: StreamingVarwinVideoWrapper — документация Varwin 18

_class_ StreamingVarwinVideo.StreamingVarwinVideoWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения (0..10)

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость (0..1)

**Пример:**

value = instance.Volume

_property_ Loop _:bool_[]
Зациклить

**Пример:**

value = instance.Loop

_property_ PlayOnAwake _:bool_[]
Воспроизвести на старте

**Пример:**

value = instance.PlayOnAwake

_property_ Length _:Any_[]
Длительность видео (в секундах)

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время (в секундах)

**Пример:**

value = instance.CurrentTime

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

Play()→None[]
Воспроизвести

**Пример:**

instance.Play()

LoadVideo()→None[]
Загрузить

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить

**Пример:**

instance.UnloadVideo()

Stop()→None[]
Остановить

**Пример:**

instance.Stop()

Pause()→None[]
Пауза

**Пример:**

instance.Pause()

ResetSpeed()→None[]
Восстановить исходную скорость воспроизведения

**Пример:**

instance.ResetSpeed()

Seek(_position:Any_)→None[]
Перемотать на секунду

**Пример:**

instance.Seek(0)

MuteAudio()→None[]
Выключить звук

**Пример:**

instance.MuteAudio()

UnmuteAudio()→None[]
Включить звук

**Пример:**

instance.UnmuteAudio()

AddPlaybackCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение окончено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPlaybackCompleted(sender):
  pass
instance.AddPlaybackCompletedHandler(OnPlaybackCompleted)

AddVideoLoadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Загружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnVideoLoaded(sender):
  pass
instance.AddVideoLoadedHandler(OnVideoLoaded)

########## _generated_TutorialBulb_TutorialBulbWrapper.html.md

# TutorialBulbWrapper[]

_class_ TutorialBulb.TutorialBulbWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ Color _:[Color]_[]
Цвет свечения

**Пример:**

value = instance.Color

IsOn()→bool[]
Включена в данный момент

**Пример:**

value = instance.IsOn()

TurnOn()→None[]
Включить

**Пример:**

instance.TurnOn()

TurnOff()→None[]
Выключить

**Пример:**

instance.TurnOff()

########## _generated_TutorialButton_TutorialButtonWrapper.html.md
Title: TutorialButtonWrapper — документация Varwin 18

_class_ TutorialButton.TutorialButtonWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

IsPressed()→bool[]
Нажата в данный момент

**Пример:**

value = instance.IsPressed()

SetPressedState()→None[]
Нажать

**Пример:**

instance.SetPressedState()

SetReleasedState()→None[]
Отжать

**Пример:**

instance.SetReleasedState()

AddPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPressed(sender):
  pass
instance.AddPressedHandler(OnPressed)

AddReleasedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Отжата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnReleased(sender):
  pass
instance.AddReleasedHandler(OnReleased)

########## _generated_TutorialDisplay_TutorialDisplayWrapper.html.md
Title: TutorialDisplayWrapper — документация Varwin 18

[Varwin]_class_ TutorialDisplay.TutorialDisplayWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ Fonts[]

Ubuntu _:Any_ _=Ellipsis_[]
Ubuntu

PtSerif _:Any_ _=Ellipsis_[]
PT Serif

RobotoMono _:Any_ _=Ellipsis_[]
Roboto Mono

BadScript _:Any_ _=Ellipsis_[]
BadScript

_class_ AlignmentHorizontalType[]

Left _:Any_ _=Ellipsis_[]
По левому краю

Center _:Any_ _=Ellipsis_[]
Посередине

Right _:Any_ _=Ellipsis_[]
По правому краю

Flush _:Any_ _=Ellipsis_[]
Заполнить

_class_ AlignmentVerticalType[]

Top _:Any_ _=Ellipsis_[]
По верхнему краю

Middle _:Any_ _=Ellipsis_[]
Посередине

Bottom _:Any_ _=Ellipsis_[]
По нижнему краю

_class_ ProportionType[]

Save _:Any_ _=Ellipsis_[]
Сохранять

NotSave _:Any_ _=Ellipsis_[]
Не сохранять

_property_ TextColor _:[Color]_[]
Цвет текста

**Пример:**

value = instance.TextColor

_property_ TextFont _:Any_[]
Шрифт

Результат:
значение из перечня:

*   TutorialDisplayWrapper.Fonts.Ubuntu

*   TutorialDisplayWrapper.Fonts.PtSerif

*   TutorialDisplayWrapper.Fonts.RobotoMono

*   TutorialDisplayWrapper.Fonts.BadScript

**Пример:**

value = instance.TextFont

_property_ FontSizeMax _:float_[]
Максимальный размер шрифта

**Пример:**

value = instance.FontSizeMax

_property_ FontSizeMin _:float_[]
Минимальный размер шрифта

**Пример:**

value = instance.FontSizeMin

_property_ HorizontalAlignment _:Any_[]
Горизонтальное выравнивание

Результат:
значение из перечня:

*   TutorialDisplayWrapper.AlignmentHorizontalType.Left

*   TutorialDisplayWrapper.AlignmentHorizontalType.Center

*   TutorialDisplayWrapper.AlignmentHorizontalType.Right

*   TutorialDisplayWrapper.AlignmentHorizontalType.Flush

**Пример:**

value = instance.HorizontalAlignment

_property_ VerticalAlignment _:Any_[]
Вертикальное выравнивание

Результат:
значение из перечня:

*   TutorialDisplayWrapper.AlignmentVerticalType.Top

*   TutorialDisplayWrapper.AlignmentVerticalType.Middle

*   TutorialDisplayWrapper.AlignmentVerticalType.Bottom

**Пример:**

value = instance.VerticalAlignment

_property_ BoldStyle _:bool_[]
Жирный стиль шрифта

**Пример:**

value = instance.BoldStyle

_property_ ItalicStyle _:bool_[]
Курсивный стиль шрифта

**Пример:**

value = instance.ItalicStyle

_property_ UnderlinedStyle _:bool_[]
Подчеркнутый стиль шрифта

**Пример:**

value = instance.UnderlinedStyle

_property_ StrikethroughStyle _:bool_[]
Зачеркнутый стиль шрифта

**Пример:**

value = instance.StrikethroughStyle

_property_ Proportion _:Any_[]
> [value] пропорции текста при изменении пропорций панели

Результат:
значение из перечня:

*   TutorialDisplayWrapper.ProportionType.Save

*   TutorialDisplayWrapper.ProportionType.NotSave

**Пример:**

value = instance.Proportion

_property_ PaddingLeft _:float_[]
Отступ текста слева

**Пример:**

value = instance.PaddingLeft

_property_ PaddingRight _:float_[]
Отступ текста справа

**Пример:**

value = instance.PaddingRight

_property_ PaddingTop _:float_[]
Отступ текста сверху

**Пример:**

value = instance.PaddingTop

_property_ PaddingBottom _:float_[]
Отступ текста снизу

**Пример:**

value = instance.PaddingBottom

SetText(_text:Any_)→None[]
Задать текст

**Пример:**

instance.SetText(0)

########## _generated_VBotBoy_VBotBoyWrapper.html.md
Title: VBotBoyWrapper — документация Varwin 18

[Varwin]_class_ VBotBoy.VBotBoyWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ RotationDirection[]

Clockwise _:Any_ _=Ellipsis_[]
По часовой стрелке

Counterclockwise _:Any_ _=Ellipsis_[]
Против часовой стрелки

_class_ MovementDirection[]

Forward _:Any_ _=Ellipsis_[]
Вперед

Backward _:Any_ _=Ellipsis_[]
Назад

Left _:Any_ _=Ellipsis_[]
Влево

Right _:Any_ _=Ellipsis_[]
Вправо

_class_ MovementPace[]

Walk _:Any_ _=Ellipsis_[]
Шагом

Run _:Any_ _=Ellipsis_[]
Бегом

_class_ TextBubbleHideType[]

Automatic _:Any_ _=Ellipsis_[]
Автоматически

Never _:Any_ _=Ellipsis_[]
Никогда

SetMaxTraversableSlope(_slope:float_)→None[]
Задать максимальный угол подъема

**Пример:**

instance.SetMaxTraversableSlope(0)

SetMaxStepHeight(_slope:float_)→None[]
Задать максимальную высоту шага

**Пример:**

instance.SetMaxStepHeight(0)

SetMinObjectDistance(_objectDistance:float_)→None[]
Задать расстояние остановки перед объектом

**Пример:**

instance.SetMinObjectDistance(0)

_async_ RotateByAngle(_angle:float_, _rotationDirection:int_, _time:float_)→None[]
Повернуть на [angle] градусов [rotationDirection] за [time] сек

Параметры:
**(****int****)** (_rotationDirection_) –

значение из перечня:

*   VBotBoyWrapper.RotationDirection.Clockwise

*   VBotBoyWrapper.RotationDirection.Counterclockwise

**Пример:**

await instance.RotateByAngle(0, VBotBoyWrapper.RotationDirection.Clockwise, 0)

MoveInfinite(_movementDirection:int_, _movementPace:int_)→None[]
Двигаться [movementDirection] [movementPace] до остановки

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotBoyWrapper.MovementDirection.Forward

    *   VBotBoyWrapper.MovementDirection.Backward

    *   VBotBoyWrapper.MovementDirection.Left

    *   VBotBoyWrapper.MovementDirection.Right

*   **(****int****)** –

значение из перечня:

    *   VBotBoyWrapper.MovementPace.Walk

    *   VBotBoyWrapper.MovementPace.Run

**Пример:**

instance.MoveInfinite(VBotBoyWrapper.MovementDirection.Forward, VBotBoyWrapper.MovementPace.Walk)

_async_ MoveByMeters(_movementDirection:int_, _movementPace:int_, _distance:float_)→None[]
Передвинуться [movementDirection] [movementPace] на расстояние [distance] м

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotBoyWrapper.MovementDirection.Forward

    *   VBotBoyWrapper.MovementDirection.Backward

    *   VBotBoyWrapper.MovementDirection.Left

    *   VBotBoyWrapper.MovementDirection.Right

*   **(****int****)** –

значение из перечня:

    *   VBotBoyWrapper.MovementPace.Walk

    *   VBotBoyWrapper.MovementPace.Run

**Пример:**

await instance.MoveByMeters(VBotBoyWrapper.MovementDirection.Forward, VBotBoyWrapper.MovementPace.Walk, 0)

_async_ MoveToObject(_movementPace:int_, _wrapper:[Object]_)→None[]
Двигаться [movementPace] в сторону объекта [wrapper]

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotBoyWrapper.MovementPace.Walk

    *   VBotBoyWrapper.MovementPace.Run

*   **(****Object****)** (_wrapper_) – объект сцены

**Пример:**

await instance.MoveToObject(VBotBoyWrapper.MovementPace.Walk, sceneObject)

_async_ MoveAlongPath(_movementPace:int_, _points:Any_)→None[]
Двигаться [movementPace] по маршруту [points]

Параметры:
**(****int****)** (_movementPace_) –

значение из перечня:

*   VBotBoyWrapper.MovementPace.Walk

*   VBotBoyWrapper.MovementPace.Run

**Пример:**

await instance.MoveAlongPath(VBotBoyWrapper.MovementPace.Walk, 0)

PausePath()→None[]
Приостановить движение по маршруту

**Пример:**

instance.PausePath()

ContinuePath()→None[]
Продолжить движение по маршруту

**Пример:**

instance.ContinuePath()

StopMovement()→None[]
Остановить движение

**Пример:**

instance.StopMovement()

SetShowTextBubbleHideType(_hideType:int_)→None[]
Задать тип скрывания говоримого текста

Параметры:
**(****int****)** (_hideType_) –

значение из перечня:

*   VBotBoyWrapper.TextBubbleHideType.Automatic

*   VBotBoyWrapper.TextBubbleHideType.Never

**Пример:**

instance.SetShowTextBubbleHideType(VBotBoyWrapper.TextBubbleHideType.Automatic)

SetShowTextBubble(_show:bool_)→None[]
Задать отображение говоримого текста

**Пример:**

instance.SetShowTextBubble(False)

SayText(_text:str_)→None[]
Сказать

**Пример:**

instance.SayText("text")

SayTextWith(_header:str_, _text:str_)→None[]
Сказать заголовок: [header] текст: [text]

**Пример:**

instance.SayTextWith("text", "text")

StopSpeaking()→None[]
Перестать говорить

**Пример:**

instance.StopSpeaking()

AddBotTargetReachedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Целевой объект достигнут

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBotTargetReached(target, sender):
  pass
instance.AddBotTargetReachedHandler(OnBotTargetReached)

AddBotPathPointReachedHandler(_handler:Callable[[int,[Object],[Object]],CoroutineType]_)→None[]
Точка пути достигнута

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   id (int): id

*   point (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBotPathPointReached(id, point, sender):
  pass
instance.AddBotPathPointReachedHandler(OnBotPathPointReached)

AddSpeechCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Фраза произнесена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnSpeechCompleted(sender):
  pass
instance.AddSpeechCompletedHandler(OnSpeechCompleted)

########## _generated_VBotGirl_VBotGirlWrapper.html.md
Title: VBotGirlWrapper — документация Varwin 18

[Varwin]_class_ VBotGirl.VBotGirlWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ RotationDirection[]

Clockwise _:Any_ _=Ellipsis_[]
По часовой стрелке

Counterclockwise _:Any_ _=Ellipsis_[]
Против часовой стрелки

_class_ MovementDirection[]

Forward _:Any_ _=Ellipsis_[]
Вперед

Backward _:Any_ _=Ellipsis_[]
Назад

Left _:Any_ _=Ellipsis_[]
Влево

Right _:Any_ _=Ellipsis_[]
Вправо

_class_ MovementPace[]

Walk _:Any_ _=Ellipsis_[]
Шагом

Run _:Any_ _=Ellipsis_[]
Бегом

_class_ TextBubbleHideType[]

Automatic _:Any_ _=Ellipsis_[]
Автоматически

Never _:Any_ _=Ellipsis_[]
Никогда

SetMaxTraversableSlope(_slope:float_)→None[]
Задать максимальный угол подъема

**Пример:**

instance.SetMaxTraversableSlope(0)

SetMaxStepHeight(_slope:float_)→None[]
Задать максимальную высоту шага

**Пример:**

instance.SetMaxStepHeight(0)

SetMinObjectDistance(_objectDistance:float_)→None[]
Задать расстояние остановки перед объектом

**Пример:**

instance.SetMinObjectDistance(0)

_async_ RotateByAngle(_angle:float_, _rotationDirection:int_, _time:float_)→None[]
Повернуть на [angle] градусов [rotationDirection] за [time] сек

Параметры:
**(****int****)** (_rotationDirection_) –

значение из перечня:

*   VBotGirlWrapper.RotationDirection.Clockwise

*   VBotGirlWrapper.RotationDirection.Counterclockwise

**Пример:**

await instance.RotateByAngle(0, VBotGirlWrapper.RotationDirection.Clockwise, 0)

MoveInfinite(_movementDirection:int_, _movementPace:int_)→None[]
Двигаться [movementDirection] [movementPace] до остановки

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotGirlWrapper.MovementDirection.Forward

    *   VBotGirlWrapper.MovementDirection.Backward

    *   VBotGirlWrapper.MovementDirection.Left

    *   VBotGirlWrapper.MovementDirection.Right

*   **(****int****)** –

значение из перечня:

    *   VBotGirlWrapper.MovementPace.Walk

    *   VBotGirlWrapper.MovementPace.Run

**Пример:**

instance.MoveInfinite(VBotGirlWrapper.MovementDirection.Forward, VBotGirlWrapper.MovementPace.Walk)

_async_ MoveByMeters(_movementDirection:int_, _movementPace:int_, _distance:float_)→None[]
Передвинуться [movementDirection] [movementPace] на расстояние [distance] м

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotGirlWrapper.MovementDirection.Forward

    *   VBotGirlWrapper.MovementDirection.Backward

    *   VBotGirlWrapper.MovementDirection.Left

    *   VBotGirlWrapper.MovementDirection.Right

*   **(****int****)** –

значение из перечня:

    *   VBotGirlWrapper.MovementPace.Walk

    *   VBotGirlWrapper.MovementPace.Run

**Пример:**

await instance.MoveByMeters(VBotGirlWrapper.MovementDirection.Forward, VBotGirlWrapper.MovementPace.Walk, 0)

_async_ MoveToObject(_movementPace:int_, _wrapper:[Object]_)→None[]
Двигаться [movementPace] в сторону объекта [wrapper]

Параметры:
*   **(****int****)** (_movementPace_) –

значение из перечня:

    *   VBotGirlWrapper.MovementPace.Walk

    *   VBotGirlWrapper.MovementPace.Run

*   **(****Object****)** (_wrapper_) – объект сцены

**Пример:**

await instance.MoveToObject(VBotGirlWrapper.MovementPace.Walk, sceneObject)

_async_ MoveAlongPath(_movementPace:int_, _points:Any_)→None[]
Двигаться [movementPace] по маршруту [points]

Параметры:
**(****int****)** (_movementPace_) –

значение из перечня:

*   VBotGirlWrapper.MovementPace.Walk

*   VBotGirlWrapper.MovementPace.Run

**Пример:**

await instance.MoveAlongPath(VBotGirlWrapper.MovementPace.Walk, 0)

PausePath()→None[]
Приостановить движение по маршруту

**Пример:**

instance.PausePath()

ContinuePath()→None[]
Продолжить движение по маршруту

**Пример:**

instance.ContinuePath()

StopMovement()→None[]
Остановить движение

**Пример:**

instance.StopMovement()

SetShowTextBubbleHideType(_hideType:int_)→None[]
Задать тип скрывания говоримого текста

Параметры:
**(****int****)** (_hideType_) –

значение из перечня:

*   VBotGirlWrapper.TextBubbleHideType.Automatic

*   VBotGirlWrapper.TextBubbleHideType.Never

**Пример:**

instance.SetShowTextBubbleHideType(VBotGirlWrapper.TextBubbleHideType.Automatic)

SetShowTextBubble(_show:bool_)→None[]
Задать отображение говоримого текста

**Пример:**

instance.SetShowTextBubble(False)

SayText(_text:str_)→None[]
Сказать

**Пример:**

instance.SayText("text")

SayTextWith(_header:str_, _text:str_)→None[]
Сказать заголовок: [header] текст: [text]

**Пример:**

instance.SayTextWith("text", "text")

StopSpeaking()→None[]
Перестать говорить

**Пример:**

instance.StopSpeaking()

AddBotTargetReachedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Целевой объект достигнут

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBotTargetReached(target, sender):
  pass
instance.AddBotTargetReachedHandler(OnBotTargetReached)

AddBotPathPointReachedHandler(_handler:Callable[[int,[Object],[Object]],CoroutineType]_)→None[]
Точка пути достигнута

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   id (int): id

*   point (Object): объект сцены

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnBotPathPointReached(id, point, sender):
  pass
instance.AddBotPathPointReachedHandler(OnBotPathPointReached)

AddSpeechCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Фраза произнесена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnSpeechCompleted(sender):
  pass
instance.AddSpeechCompletedHandler(OnSpeechCompleted)

########## _generated_VCone_VConeWrapper.html.md

# VConeWrapper[]

_class_ VCone.VConeWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VCube_VCubeWrapper.html.md

# VCubeWrapper[]

_class_ VCube.VCubeWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VCylinder_VCylinderWrapper.html.md

# VCylinderWrapper[]

_class_ VCylinder.VCylinderWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VDirectionalLight_VDirectionalLightWrapper.html.md
Title: VDirectionalLightWrapper — документация Varwin 18

_class_ VDirectionalLight.VDirectionalLightWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LightShadows[]

None_ _:Any_ _=Ellipsis_[]
Без теней

Hard _:Any_ _=Ellipsis_[]
Жесткие тени

Soft _:Any_ _=Ellipsis_[]
Мягкие тени

_property_ Color _:[Color]_[]
Цвет свечения

**Пример:**

value = instance.Color

_property_ Intensity _:float_[]
Интенсивность света

**Пример:**

value = instance.Intensity

_property_ Shadows _:Any_[]
Тип теней

Результат:
значение из перечня:

*   VDirectionalLightWrapper.LightShadows.None

*   VDirectionalLightWrapper.LightShadows.Hard

*   VDirectionalLightWrapper.LightShadows.Soft

**Пример:**

value = instance.Shadows

_property_ ShadowStrength _:float_[]
Интенсивность тени

**Пример:**

value = instance.ShadowStrength

########## _generated_VEmptyObject_VEmptyObjectWrapper.html.md

# VEmptyObjectWrapper[]

_class_ VEmptyObject.VEmptyObjectWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VHexagon_VHexagonWrapper.html.md

# VHexagonWrapper[]

_class_ VHexagon.VHexagonWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VPanorama180_VPanorama180Wrapper.html.md
Title: VPanorama180Wrapper — документация Varwin 18

_class_ VPanorama180.VPanorama180Wrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   VPanorama180Wrapper.PlayerLockOptions.Lock

*   VPanorama180Wrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

Load()→None[]
Загрузить изображение панорамы

**Пример:**

instance.Load()

Unload()→None[]
Выгрузить изображение панорамы

**Пример:**

instance.Unload()

AddPanoramaImageLoadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Изображение загружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPanoramaImageLoaded(sender):
  pass
instance.AddPanoramaImageLoadedHandler(OnPanoramaImageLoaded)

AddPanoramaImageUnloadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Изображение выгружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPanoramaImageUnloaded(sender):
  pass
instance.AddPanoramaImageUnloadedHandler(OnPanoramaImageUnloaded)

########## _generated_VPanorama_VPanoramaWrapper.html.md
Title: VPanoramaWrapper — документация Varwin 18

_class_ VPanorama.VPanoramaWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   VPanoramaWrapper.PlayerLockOptions.Lock

*   VPanoramaWrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

Load()→None[]
Загрузить изображение панорамы

**Пример:**

instance.Load()

Unload()→None[]
Выгрузить изображение панорамы

**Пример:**

instance.Unload()

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

AddPanoramaImageLoadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Изображение загружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPanoramaImageLoaded(sender):
  pass
instance.AddPanoramaImageLoadedHandler(OnPanoramaImageLoaded)

AddPanoramaImageUnloadedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Изображение выгружено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPanoramaImageUnloaded(sender):
  pass
instance.AddPanoramaImageUnloadedHandler(OnPanoramaImageUnloaded)

########## _generated_VPlane_VPlaneWrapper.html.md

# VPlaneWrapper[]

_class_ VPlane.VPlaneWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VPointLight_VPointLightWrapper.html.md
Title: VPointLightWrapper — документация Varwin 18

_class_ VPointLight.VPointLightWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LightShadows[]

None_ _:Any_ _=Ellipsis_[]
Без теней

Hard _:Any_ _=Ellipsis_[]
Жесткие тени

Soft _:Any_ _=Ellipsis_[]
Мягкие тени

_property_ Range _:float_[]
Дальность света

**Пример:**

value = instance.Range

_property_ Intensity _:float_[]
Интенсивность света

**Пример:**

value = instance.Intensity

_property_ Color _:[Color]_[]
Цвет свечения

**Пример:**

value = instance.Color

_property_ Shadows _:Any_[]
Тип теней

Результат:
значение из перечня:

*   VPointLightWrapper.LightShadows.None

*   VPointLightWrapper.LightShadows.Hard

*   VPointLightWrapper.LightShadows.Soft

**Пример:**

value = instance.Shadows

_property_ ShadowStrength _:float_[]
Интенсивность тени

**Пример:**

value = instance.ShadowStrength

########## _generated_VPyramid_VPyramidWrapper.html.md

# VPyramidWrapper[]

_class_ VPyramid.VPyramidWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VSmile_VSmileWrapper.html.md
Title: VSmileWrapper — документация Varwin 18

_class_ VSmile.VSmileWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ SmileState[]

Happy _:Any_ _=Ellipsis_[]
Радостный

Neutral _:Any_ _=Ellipsis_[]
Нейтральный

Sad _:Any_ _=Ellipsis_[]
Грустный

None_ _:Any_ _=Ellipsis_[]
Отсутствует

IsState(_state:int_)→bool[]
[state] в данный момент

Параметры:
**(****int****)** (_state_) –

значение из перечня:

*   VSmileWrapper.SmileState.Happy

*   VSmileWrapper.SmileState.Neutral

*   VSmileWrapper.SmileState.Sad

*   VSmileWrapper.SmileState.None

**Пример:**

value = instance.IsState(VSmileWrapper.SmileState.Happy)

SetState(_state:int_)→None[]
Задать настроение

Параметры:
**(****int****)** (_state_) –

значение из перечня:

*   VSmileWrapper.SmileState.Happy

*   VSmileWrapper.SmileState.Neutral

*   VSmileWrapper.SmileState.Sad

*   VSmileWrapper.SmileState.None

**Пример:**

instance.SetState(VSmileWrapper.SmileState.Happy)

########## _generated_VSphere_VSphereWrapper.html.md

# VSphereWrapper[]

_class_ VSphere.VSphereWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## _generated_VSpotLight_VSpotLightWrapper.html.md
Title: VSpotLightWrapper — документация Varwin 18

_class_ VSpotLight.VSpotLightWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LightShadows[]

None_ _:Any_ _=Ellipsis_[]
Без теней

Hard _:Any_ _=Ellipsis_[]
Жесткие тени

Soft _:Any_ _=Ellipsis_[]
Мягкие тени

_property_ Range _:float_[]
Дальность света

**Пример:**

value = instance.Range

_property_ Intensity _:float_[]
Интенсивность света

**Пример:**

value = instance.Intensity

_property_ Color _:[Color]_[]
Цвет свечения

**Пример:**

value = instance.Color

_property_ Shadows _:Any_[]
Тип теней

Результат:
значение из перечня:

*   VSpotLightWrapper.LightShadows.None

*   VSpotLightWrapper.LightShadows.Hard

*   VSpotLightWrapper.LightShadows.Soft

**Пример:**

value = instance.Shadows

_property_ ShadowStrength _:float_[]
Интенсивность тени

**Пример:**

value = instance.ShadowStrength

_property_ Angle _:float_[]
Угол прожектора

**Пример:**

value = instance.Angle

########## _generated_VText_VTextWrapper.html.md
Title: VTextWrapper — документация Varwin 18

[Varwin]_class_ VText.VTextWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ Fonts[]

Ubuntu _:Any_ _=Ellipsis_[]
Ubuntu

PtSerif _:Any_ _=Ellipsis_[]
PT Serif

RobotoMono _:Any_ _=Ellipsis_[]
Roboto Mono

BadScript _:Any_ _=Ellipsis_[]
BadScript

_class_ HorizontalAlignment[]

Left _:Any_ _=Ellipsis_[]
По левому краю

Right _:Any_ _=Ellipsis_[]
По правому краю

Center _:Any_ _=Ellipsis_[]
Посередине

Flush _:Any_ _=Ellipsis_[]
Заполнить

_class_ VerticalAlignment[]

Top _:Any_ _=Ellipsis_[]
По верхнему краю

Middle _:Any_ _=Ellipsis_[]
Посередине

Bottom _:Any_ _=Ellipsis_[]
По нижнему краю

_class_ KeepProportionOptions[]

Save _:Any_ _=Ellipsis_[]
Сохранять

Keep _:Any_ _=Ellipsis_[]
Не сохранять

_property_ TextColor _:[Color]_[]
Цвет текста

**Пример:**

value = instance.TextColor

_property_ PanelColor _:[Color]_[]
Цвет панели

**Пример:**

value = instance.PanelColor

_property_ Size _:float_[]
Размер шрифта

**Пример:**

value = instance.Size

_property_ MaxFontSize _:float_[]
Максимальный [value] размер шрифта

**Пример:**

value = instance.MaxFontSize

_property_ MinFontSize _:float_[]
Минимальный [value] размер шрифта

**Пример:**

value = instance.MinFontSize

_property_ Bold _:bool_[]
Жирный стиль шрифта

**Пример:**

value = instance.Bold

_property_ Italic _:bool_[]
Курсивный стиль шрифта

**Пример:**

value = instance.Italic

_property_ Font _:Any_[]
Шрифт

Результат:
значение из перечня:

*   VTextWrapper.Fonts.Ubuntu

*   VTextWrapper.Fonts.PtSerif

*   VTextWrapper.Fonts.RobotoMono

*   VTextWrapper.Fonts.BadScript

**Пример:**

value = instance.Font

_property_ Underline _:bool_[]
Подчеркнутый стиль шрифта

**Пример:**

value = instance.Underline

_property_ Strikethrough _:bool_[]
Зачеркнутый стиль шрифта

**Пример:**

value = instance.Strikethrough

_property_ HorizontalTextAlignment _:Any_[]
Горизонтальное выравнивание

Результат:
значение из перечня:

*   VTextWrapper.HorizontalAlignment.Left

*   VTextWrapper.HorizontalAlignment.Right

*   VTextWrapper.HorizontalAlignment.Center

*   VTextWrapper.HorizontalAlignment.Flush

**Пример:**

value = instance.HorizontalTextAlignment

_property_ VerticalTextAlignment _:Any_[]
Вертикальное выравнивание

Результат:
значение из перечня:

*   VTextWrapper.VerticalAlignment.Top

*   VTextWrapper.VerticalAlignment.Middle

*   VTextWrapper.VerticalAlignment.Bottom

**Пример:**

value = instance.VerticalTextAlignment

_property_ TopPadding _:int_[]
Отступ текста сверху

**Пример:**

value = instance.TopPadding

_property_ BottomPadding _:int_[]
Отступ текста снизу

**Пример:**

value = instance.BottomPadding

_property_ LeftPadding _:int_[]
Отступ текста слева

**Пример:**

value = instance.LeftPadding

_property_ RightPadding _:int_[]
Отступ текста справа

**Пример:**

value = instance.RightPadding

_property_ KeepTextProportions _:Any_[]
> [value] пропорции текста при изменении пропорций панели

Результат:
значение из перечня:

*   VTextWrapper.KeepProportionOptions.Save

*   VTextWrapper.KeepProportionOptions.Keep

**Пример:**

value = instance.KeepTextProportions

_property_ SortingOrder _:int_[]
Порядок отрисовки

**Пример:**

value = instance.SortingOrder

SetText(_value:str_)→None[]
Задать текст

**Пример:**

instance.SetText("text")

GetText()→str[]
Получить текущий текст

**Пример:**

value = instance.GetText()

########## _generated_Varwin.html.md

# Varwin[]

*   [Enum]
*   [Application]
*   [Debug]
*   [Color]
*   [Vector3]
*   [Math]
*   [StringUtils]
*   [Random]
*   [Async]
*   [Project]
*   [WaitForSeconds]
*   [WaitForEndOfFrame]
*   [WaitWhile]
*   [ListUtils]
*   [Range]
*   [Variable]
*   [Coroutine]
*   [DynamicValueDictionary]
*   [Event]
*   [Method]
*   [Property]
*   [Requests]
*   [InteractionBehaviour]
*   [MotionBehaviour]
*   [PhysicsBehaviour]
*   [RotateBehaviour]
*   [ScaleBehaviour]
*   [VisualizationBehaviour]
*   [Object]
*   [Objects]
*   [Cloning]
*   [Collisions]
*   [UserType]
*   [DynamicModuleProvider]

########## _generated_VarwinAudio_VarwinAudioWrapper.html.md
Title: VarwinAudioWrapper — документация Varwin 18

_class_ VarwinAudio.VarwinAudioWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LoopState[]

Looped _:Any_ _=Ellipsis_[]
Зацикленное воспроизведение

Unlooped _:Any_ _=Ellipsis_[]
Не зацикленное воспроизведение

_property_ PlaybackLoopState _:Any_[]Результат:
значение из перечня:

*   VarwinAudioWrapper.LoopState.Looped

*   VarwinAudioWrapper.LoopState.Unlooped

**Пример:**

value = instance.PlaybackLoopState

_property_ Volume _:float_[]
Громкость [0..1]

**Пример:**

value = instance.Volume

_property_ Speed _:float_[]
Скорость воспроизведения

**Пример:**

value = instance.Speed

_property_ Length _:Any_[]
Длина аудио, с.

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время, с.

**Пример:**

value = instance.CurrentTime

IsPlaying()→bool[]
Воспроизводится в данный момент

**Пример:**

value = instance.IsPlaying()

IsPaused()→bool[]
На паузе в данный момент

**Пример:**

value = instance.IsPaused()

IsStopped()→bool[]
Остановлено в данный момент

**Пример:**

value = instance.IsStopped()

_async_ PlaySound()→None[]
Воспроизвести

**Пример:**

await instance.PlaySound()

_async_ StopSound()→None[]
Остановить

**Пример:**

await instance.StopSound()

_async_ PauseSound()→None[]
Поставить на паузу

**Пример:**

await instance.PauseSound()

Seek(_position:float_)→None[]
Перемотать на время [position] с.

**Пример:**

instance.Seek(0)

AddPlaybackCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение завершено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnPlaybackCompleted(sender):
  pass
instance.AddPlaybackCompletedHandler(OnPlaybackCompleted)

########## _generated_VarwinBasicContentPack.html.md

# Базовые объекты[]

*   [ARMarker]
*   [BallsBox]
*   [Basketball]
*   [Basketball_Hoop]
*   [BoxCollider]
*   [CapsuleCollider]
*   [CustomZone]
*   [DefaultSpawnPoint]
*   [Player]
*   [SKCoin]
*   [SKFlyingDrone]
*   [SKHumanoidBot]
*   [SKJoystick]
*   [SKLadder]
*   [SKSimpleBot]
*   [SphereCollider]
*   [StreamingVarwinVideo]
*   [StreamingVarwinVideo180]
*   [StreamingVarwinVideo360]
*   [TutorialBulb]
*   [TutorialButton]
*   [TutorialDisplay]
*   [VarwinAudio]
*   [VarwinImage]
*   [VarwinModel]
*   [VarwinVideo]
*   [VarwinVideo180]
*   [VarwinVideo360]
*   [VBotBoy]
*   [VBotGirl]
*   [VCone]
*   [VCube]
*   [VCylinder]
*   [VDirectionalLight]
*   [VEmptyObject]
*   [VHexagon]
*   [VPanorama]
*   [VPanorama180]
*   [VPlane]
*   [VPointLight]
*   [VPyramid]
*   [VSmile]
*   [VSphere]
*   [VSpotLight]
*   [VText]
*   [Woodenoldtable]

########## _generated_VarwinImage_VarwinImageWrapper.html.md

# VarwinImageWrapper[]

_class_ VarwinImage.VarwinImageWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_property_ SortingOrder _:int_[]
Порядок отрисовки

**Пример:**

value = instance.SortingOrder

########## _generated_VarwinModel_VarwinModelWrapper.html.md
Title: VarwinModelWrapper — документация Varwin 18

[Varwin]_class_ VarwinModel.VarwinModelWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ AnimationPlayTypeOptions[]

Direct _:Any_ _=Ellipsis_[]
Прямое

Reverse _:Any_ _=Ellipsis_[]
Обратное

PingPong _:Any_ _=Ellipsis_[]
Пинг-понг

_class_ LoopOptions[]

Looped _:Any_ _=Ellipsis_[]
Зациклено

NotLooped _:Any_ _=Ellipsis_[]
Не зациклено

_property_ AnimationPlaybackMode _:Any_[]
Воспроизведение анимации

Результат:
значение из перечня:

*   VarwinModelWrapper.AnimationPlayTypeOptions.Direct

*   VarwinModelWrapper.AnimationPlayTypeOptions.Reverse

*   VarwinModelWrapper.AnimationPlayTypeOptions.PingPong

**Пример:**

value = instance.AnimationPlaybackMode

_property_ LoopMode _:Any_[]
Воспроизведение анимации

Результат:
значение из перечня:

*   VarwinModelWrapper.LoopOptions.Looped

*   VarwinModelWrapper.LoopOptions.NotLooped

**Пример:**

value = instance.LoopMode

_property_ AnimationSpeed _:float_[]
Скорость воспроизведения анимации

**Пример:**

value = instance.AnimationSpeed

SetAnimationByIndex(_index:int_)→None[]
Запустить анимацию №

**Пример:**

instance.SetAnimationByIndex(0)

PlayAnimation()→None[]
Воспроизвести текущую анимацию

**Пример:**

instance.PlayAnimation()

PauseAnimation()→None[]
Приостановить текущую анимацию

**Пример:**

instance.PauseAnimation()

StopAnimation()→None[]
Остановить текущую анимацию

**Пример:**

instance.StopAnimation()

AddAnimationFinishedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Анимация завершена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   index (int): index

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnAnimationFinished(index, sender):
  pass
instance.AddAnimationFinishedHandler(OnAnimationFinished)

AddAnimationPausedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Анимация приостановлена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   index (int): index

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnAnimationPaused(index, sender):
  pass
instance.AddAnimationPausedHandler(OnAnimationPaused)

AddAnimationStoppedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Анимация остановлена

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   index (int): index

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnAnimationStopped(index, sender):
  pass
instance.AddAnimationStoppedHandler(OnAnimationStopped)

########## _generated_VarwinVideo180_VarwinVideo180Wrapper.html.md
Title: VarwinVideo180Wrapper — документация Varwin 18

_class_ VarwinVideo180.VarwinVideo180Wrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_class_ LoopBehaviourOptions[]

Looped _:Any_ _=Ellipsis_[]
Зацикленное

NotLooped _:Any_ _=Ellipsis_[]
Не зацикленное

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   VarwinVideo180Wrapper.PlayerLockOptions.Lock

*   VarwinVideo180Wrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения [0..10]

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость [0..1]

**Пример:**

value = instance.Volume

_property_ SetLoopBehaviour _:Any_[]
Воспроизведение

Результат:
значение из перечня:

*   VarwinVideo180Wrapper.LoopBehaviourOptions.Looped

*   VarwinVideo180Wrapper.LoopBehaviourOptions.NotLooped

**Пример:**

value = instance.SetLoopBehaviour

_property_ Length _:Any_[]
Длина видео, с.

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время, с

**Пример:**

value = instance.CurrentTime

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

IsPaused()→bool[]
На паузе в данный момент

**Пример:**

value = instance.IsPaused()

IsStopped()→bool[]
Остановлено

**Пример:**

value = instance.IsStopped()

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

ShowPlayer()→None[]
Отобразить плеер

**Пример:**

instance.ShowPlayer()

HidePlayer()→None[]
Скрыть плеер

**Пример:**

instance.HidePlayer()

_async_ LoadAndPlay()→None[]
Воспроизвести

**Пример:**

await instance.LoadAndPlay()

_async_ Pause()→None[]
Поставить на паузу

**Пример:**

await instance.Pause()

_async_ Stop()→None[]
Остановить

**Пример:**

await instance.Stop()

Seek(_position:Any_)→None[]
Перемотать на время [position] с.

**Пример:**

instance.Seek(0)

LoadVideo()→None[]
Загрузить видео

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить видео

**Пример:**

instance.UnloadVideo()

AddCloseButtonPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Кнопка закрытия нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCloseButtonPressed(sender):
  pass
instance.AddCloseButtonPressedHandler(OnCloseButtonPressed)

AddCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение завершено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCompleted(sender):
  pass
instance.AddCompletedHandler(OnCompleted)

########## _generated_VarwinVideo360_VarwinVideo360Wrapper.html.md
Title: VarwinVideo360Wrapper — документация Varwin 18

_class_ VarwinVideo360.VarwinVideo360Wrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LoopBehaviourOptions[]

Looped _:Any_ _=Ellipsis_[]
Зацикленное

NotLooped _:Any_ _=Ellipsis_[]
Не зацикленное

_class_ PlayerLockOptions[]

Lock _:Any_ _=Ellipsis_[]
Блокировать игрока

DontLock _:Any_ _=Ellipsis_[]
Не блокировать игрока

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения [0..10]

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость [0..1]

**Пример:**

value = instance.Volume

_property_ SetLoopBehaviour _:Any_[]
Воспроизведение

Результат:
значение из перечня:

*   VarwinVideo360Wrapper.LoopBehaviourOptions.Looped

*   VarwinVideo360Wrapper.LoopBehaviourOptions.NotLooped

**Пример:**

value = instance.SetLoopBehaviour

_property_ Length _:Any_[]
Длина видео, с.

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время, с

**Пример:**

value = instance.CurrentTime

_property_ PlayerLockMode _:Any_[]Результат:
значение из перечня:

*   VarwinVideo360Wrapper.PlayerLockOptions.Lock

*   VarwinVideo360Wrapper.PlayerLockOptions.DontLock

**Пример:**

value = instance.PlayerLockMode

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

IsPaused()→bool[]
На паузе в данный момент

**Пример:**

value = instance.IsPaused()

IsStopped()→bool[]
Остановлено

**Пример:**

value = instance.IsStopped()

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

_async_ LoadAndPlay()→None[]
Воспроизвести

**Пример:**

await instance.LoadAndPlay()

_async_ Pause()→None[]
Поставить на паузу

**Пример:**

await instance.Pause()

_async_ Stop()→None[]
Остановить

**Пример:**

await instance.Stop()

Seek(_position:Any_)→None[]
Перемотать на время [position] с.

**Пример:**

instance.Seek(0)

LoadVideo()→None[]
Загрузить видео

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить видео

**Пример:**

instance.UnloadVideo()

TeleportPlayerInPanorama()→None[]
Телепортировать игрока

**Пример:**

instance.TeleportPlayerInPanorama()

ShowPlayer()→None[]
Отобразить плеер

**Пример:**

instance.ShowPlayer()

HidePlayer()→None[]
Скрыть плеер

**Пример:**

instance.HidePlayer()

AddCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение завершено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCompleted(sender):
  pass
instance.AddCompletedHandler(OnCompleted)

AddCloseButtonPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Кнопка закрытия нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCloseButtonPressed(sender):
  pass
instance.AddCloseButtonPressedHandler(OnCloseButtonPressed)

########## _generated_VarwinVideo_VarwinVideoWrapper.html.md
Title: VarwinVideoWrapper — документация Varwin 18

_class_ VarwinVideo.VarwinVideoWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

_class_ LoopBehaviourOptions[]

Looped _:Any_ _=Ellipsis_[]
Зацикленное

NotLooped _:Any_ _=Ellipsis_[]
Не зацикленное

_property_ Scale _:float_[]
Масштаб

**Пример:**

value = instance.Scale

_property_ Speed _:float_[]
Скорость воспроизведения [0..10]

**Пример:**

value = instance.Speed

_property_ Volume _:float_[]
Громкость [0..1]

**Пример:**

value = instance.Volume

_property_ SetLoopBehaviour _:Any_[]
Воспроизведение

Результат:
значение из перечня:

*   VarwinVideoWrapper.LoopBehaviourOptions.Looped

*   VarwinVideoWrapper.LoopBehaviourOptions.NotLooped

**Пример:**

value = instance.SetLoopBehaviour

_property_ Length _:Any_[]
Длина видео, с.

**Пример:**

value = instance.Length

_property_ CurrentTime _:Any_[]
Текущее время, с

**Пример:**

value = instance.CurrentTime

IsPlaying()→bool[]
Воспроизводится

**Пример:**

value = instance.IsPlaying()

IsPaused()→bool[]
На паузе в данный момент

**Пример:**

value = instance.IsPaused()

IsStopped()→bool[]
Остановлено

**Пример:**

value = instance.IsStopped()

IsLoading()→bool[]
Загружается

**Пример:**

value = instance.IsLoading()

_async_ LoadAndPlay()→None[]
Воспроизвести

**Пример:**

await instance.LoadAndPlay()

_async_ Pause()→None[]
Поставить на паузу

**Пример:**

await instance.Pause()

_async_ Stop()→None[]
Остановить

**Пример:**

await instance.Stop()

Seek(_position:Any_)→None[]
Перемотать на время [position] с.

**Пример:**

instance.Seek(0)

LoadVideo()→None[]
Загрузить видео

**Пример:**

instance.LoadVideo()

UnloadVideo()→None[]
Выгрузить видео

**Пример:**

instance.UnloadVideo()

ShowPlayer()→None[]
Отобразить плеер

**Пример:**

instance.ShowPlayer()

HidePlayer()→None[]
Скрыть плеер

**Пример:**

instance.HidePlayer()

AddCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Воспроизведение завершено

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCompleted(sender):
  pass
instance.AddCompletedHandler(OnCompleted)

AddCloseButtonPressedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Кнопка закрытия нажата

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnCloseButtonPressed(sender):
  pass
instance.AddCloseButtonPressedHandler(OnCloseButtonPressed)

########## _generated_Varwin_Application.html.md

# Application[]

_class_ Varwin.Application[]

Управляет приложением.

_static_ OpenUrl(_url:str_)→None[]
Открывает указанный URL в веб-браузере.

**Пример:**

Varwin.Application.OpenUrl("text")

########## _generated_Varwin_Async.html.md
Title: Async — документация Varwin 18

_class_ Varwin.Async[]

Управление асинхронными методами.

_static_ Run(_coroutine:CoroutineType_)→None[]
Запускает предоставленную сопрограмму.

Параметры:
**coroutine** – корутина без возвращаемого значения

**Пример:**

Varwin.Async.Run(Chain1())

_static_ AddStart(_handler:Callable[,CoroutineType]_)→None[]
Adds a handler function to be called during scene preparation.

Параметры:
**handler** – Asynchronous handler function

**Пример:**

async def OnStart():
  ...
Varwin.Async.AddStart(OnStart)

_static_ AddUpdate(_handler:Callable[,CoroutineType]_)→None[]
Adds a handler function that will be called every frame.

Параметры:
**handler** – Asynchronous handler function

**Пример:**

async def OnUpdate():
  ...
Varwin.Async.AddUpdate(OnUpdate)

########## _generated_Varwin_Cloning.html.md
Title: Cloning — документация Varwin 18

_class_ Varwin.Cloning[]

Реализует логику клонирования объектов.

T _=~T_[]_static_ CloneAtPosition(_target:T_, _position:[Vector3]_)→T[]
Клонирует объект в указанной позиции.

Параметры:
**(****T****)** (_target_) – объект сцены

Результат:
объект сцены

**Пример:**

result = Varwin.Cloning.CloneAtPosition(sceneObject1, Varwin.Vector3(1,0,0))

_static_ CloneAtObjectPosition(_target:T_, _targetObject:[Object]_)→T[]
Клонирует объект на место другого объекта.

Параметры:
*   **(****T****)** (_target_) – объект сцены

*   **(****Object****)** (_targetObject_) – объект сцены

Результат:
объект сцены

**Пример:**

result = Varwin.Cloning.CloneAtObjectPosition(sceneObject1, sceneObject2)

_static_ Clone(_target:T_)→T[]
Клонирует объект в его текущем положении.

Параметры:
**(****T****)** (_target_) – объект сцены

Результат:
объект сцены

**Пример:**

result = Varwin.Cloning.Clone(sceneObject1)

_static_ Destroy(_target:[Object]_)→None[]
Уничтожает один клонированный объект.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

Varwin.Cloning.Destroy(sceneObject1)

_static_ DestroyAllClones(_target:[Object]_)→None[]
Уничтожает все существующие клонированные объекты.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

Varwin.Cloning.DestroyAllClones(sceneObject1)

_static_ GetClones(_target:T_)→List[T][]
Возвращает список всех существующих объектов-клонов.

Параметры:
**(****T****)** (_target_) – объект сцены

**Пример:**

result = Varwin.Cloning.GetClones(sceneObject1)

_static_ IsCloneOfObject(_clone:[Object]_, _original:[Object]_)→bool[]
Проверяет, является ли заданный объект клоном другого конкретного объекта.

Параметры:
*   **(****Object****)** (_original_) – объект сцены

*   **(****Object****)** – объект сцены

**Пример:**

result = Varwin.Cloning.IsCloneOfObject(sceneObject1, sceneObject2)

_static_ IsClone(_clone:[Object]_)→bool[]
Проверяет, является ли заданный объект клоном.

Параметры:
**(****Object****)** (_clone_) – объект сцены

**Пример:**

result = Varwin.Cloning.IsClone(sceneObject1)

_static_ IsDestroyed(_clone:[Object]_)→bool[]
Проверяет, уничтожен ли заданный объект.

Параметры:
**(****Object****)** (_clone_) – объект сцены

**Пример:**

result = Varwin.Cloning.IsDestroyed(sceneObject1)

########## _generated_Varwin_Collisions.html.md
Title: Collisions — документация Varwin 18

[Varwin]_class_ Varwin.Collisions[]

Реализует логику столкновения объектов.

_static_ AddCollisionStartHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]_static_ AddCollisionStartHandler(_first:[Object]_, _second:[Object]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionStartHandler(_first:[Object]_, _second:List[[Object]]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionStartHandler(_first:List[[Object]]_, _second:[Object]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionStartHandler(_first:List[[Object]]_, _second:List[[Object]]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionEndHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]_static_ AddCollisionEndHandler(_first:[Object]_, _second:[Object]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionEndHandler(_first:[Object]_, _second:List[[Object]]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionEndHandler(_first:List[[Object]]_, _second:[Object]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None _static_ AddCollisionEndHandler(_first:List[[Object]]_, _second:List[[Object]]_, _handler:Callable[[[Object],[Object]],CoroutineType]_)→None

########## _generated_Varwin_Color.html.md
Title: Color — документация Varwin 18

[Varwin]_class_ Varwin.Color[]_class_ Varwin.Color(_r:float_, _g:float_, _b:float_, _a:float_)

Представляет цвет с красным, зелёным, синим и альфа-компонентами. Все компоненты — числа с плавающей точкой в диапазоне от 0,0 до 1,0 (включительно).

R _:float_[]G _:float_[]B _:float_[]A _:float_[]_static_ FromHex(_hex:str_)→[Color][]
Создает цвет из шестнадцатеричного строкового представления.

**Пример:**

result = Varwin.Color.FromHex("text")

_static_ GetRandom()→[Color][]
Создает объект Color со случайными значениями RGB.

**Пример:**

result = Varwin.Color.GetRandom()

_static_ Lerp(_a:[Color]_, _b:[Color]_, _t:float_)→[Color][]
Выполняет линейную интерполяцию между двумя цветами.

**Пример:**

result = Varwin.Color.Lerp(Varwin.Color(1,1,0,1), Varwin.Color(1,1,0,1), 0)

########## _generated_Varwin_Coroutine.html.md

# Coroutine[]

_class_ Varwin.Coroutine[]

########## _generated_Varwin_Debug.html.md
Title: Debug — документация Varwin 18

_class_ Varwin.Debug[]

Реализует логику отладки приложения.

_static_ Log(_message:Any_)→None[]
Регистрирует сообщение на информационном уровне

**Пример:**

Varwin.Debug.Log("test")

_static_ LogWarning(_message:Any_)→None[]
Регистрирует сообщение об ошибке на уровне предупреждения.

**Пример:**

Varwin.Debug.LogWarning("test")

_static_ LogError(_message:Any_)→None[]
Записывает сообщение об ошибке на уровне error.

**Пример:**

Varwin.Debug.LogError("test")

_static_ LogDeprecatedCodeError()→None[]
Выводит сообщение об ошибке использования устаревшего кода в редакторе.

**Пример:**

Varwin.Debug.LogDeprecatedCodeError()

########## _generated_Varwin_DynamicModuleProvider.html.md

# DynamicModuleProvider[]

_class_ Varwin.DynamicModuleProvider[]

########## _generated_Varwin_DynamicValueDictionary.html.md

# DynamicValueDictionary[]

_class_ Varwin.DynamicValueDictionary[]

Предоставляет возможность работы с логическими словарями.

_static_ Get(_identifier:str_)→Any[]
Возвращает значение из глобального словаря перечислений.

**Пример:**

result = Varwin.DynamicValueDictionary.Get("text")

########## _generated_Varwin_Enum.html.md

# Enum[]

_class_ Varwin.Enum[]

########## _generated_Varwin_Event.html.md

# Event[]

_class_ Varwin.Event[]

########## _generated_Varwin_InteractionBehaviour.html.md
Title: InteractionBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.InteractionBehaviour[]

_class_ TeleportState[]

Enabled _:Any_ _=Ellipsis_[]Disabled _:Any_ _=Ellipsis_[]_class_ TouchState[]

Enabled _:Any_ _=Ellipsis_[]Disabled _:Any_ _=Ellipsis_[]_class_ UseState[]

Enabled _:Any_ _=Ellipsis_[]Disabled _:Any_ _=Ellipsis_[]_class_ GrabState[]

Enabled _:Any_ _=Ellipsis_[]Disabled _:Any_ _=Ellipsis_[]_class_ ControllerHand[]

None_ _:Any_ _=Ellipsis_[]Left _:Any_ _=Ellipsis_[]Right _:Any_ _=Ellipsis_[]IsTouching()→bool[]
Возвращает истину, если до объекта дотрагиваются в данный момент. В противном случае возвращает ложь.

**Пример:**

result = instance.InteractionBehaviour.IsTouching()

IsUsing()→bool[]
Возвращает истину, если указанный объект используется игроком в данный момент. В противном случае возвращает ложь.

**Пример:**

result = instance.InteractionBehaviour.IsUsing()

IsGrabbed()→bool[]
Возвращает истину, если объект находится в руке в данный момент. В противном случае возвращает ложь.

**Пример:**

result = instance.InteractionBehaviour.IsGrabbed()

AddTouchStartedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок касается указанного объекта.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnTouchStarted(sender):
  ...
instance.InteractionBehaviour.AddTouchStartedHandler(OnTouchStarted)

AddUseStartedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок использует указанный объект. В параметры передается объект и рука, которой он используется.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (int): рука взаимодействия: значение из перечня

    *   [Varwin.InteractionBehaviour.ControllerHand.None_] (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Left (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Right (int)

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnUseStarted(hand, sender):
  ...
instance.InteractionBehaviour.AddUseStartedHandler(OnUseStarted)

AddGrabStartedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок берет в руку указанный объект. В параметры передается объект и рука, которой он был взят.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (int): рука взаимодействия: значение из перечня

    *   [Varwin.InteractionBehaviour.ControllerHand.None_] (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Left (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Right (int)

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnGrabStarted(hand, sender):
  ...
instance.InteractionBehaviour.AddGrabStartedHandler(OnGrabStarted)

AddTouchEndedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок касается указанного объекта.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnTouchEnded(sender):
  ...
instance.InteractionBehaviour.AddTouchEndedHandler(OnTouchEnded)

AddUseEndedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок использует указанный объект. В параметры передается объект и рука, которой он используется.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (int): рука взаимодействия: значение из перечня

    *   [Varwin.InteractionBehaviour.ControllerHand.None_] (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Left (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Right (int)

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnUseEnded(hand, sender):
  ...
instance.InteractionBehaviour.AddUseEndedHandler(OnUseEnded)

AddGrabEndedHandler(_handler:Callable[[int,[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда игрок берет в руку указанный объект. В параметры передается объект и рука, которой он был взят.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   hand (int): рука взаимодействия: значение из перечня

    *   [Varwin.InteractionBehaviour.ControllerHand.None_] (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Left (int)

    *   Varwin.InteractionBehaviour.ControllerHand.Right (int)

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnGrabEnded(hand, sender):
  ...
instance.InteractionBehaviour.AddGrabEndedHandler(OnGrabEnded)

_property_ CanTeleport _:int_[]
Задает, можно ли игроку телепортироваться или ходить по объекту.

Результат:
значение из перечня

*   Varwin.InteractionBehaviour.TeleportState.Enabled

*   Varwin.InteractionBehaviour.TeleportState.Disabled

**Пример:**

result = instance.InteractionBehaviour.CanTeleport

_property_ CanTouch _:int_[]
Задает, можно ли игроку взаимодействовать с объектом с помощью механики касания.

Результат:
значение из перечня

*   Varwin.InteractionBehaviour.TouchState.Enabled

*   Varwin.InteractionBehaviour.TouchState.Disabled

**Пример:**

result = instance.InteractionBehaviour.CanTouch

_property_ CanUse _:int_[]
Задает, можно ли игроку взаимодействовать с объектом с помощью механики использования (нажатия на объект).

Результат:
значение из перечня

*   Varwin.InteractionBehaviour.UseState.Enabled

*   Varwin.InteractionBehaviour.UseState.Disabled

**Пример:**

result = instance.InteractionBehaviour.CanUse

_property_ CanGrab _:int_[]
Задает, можно ли игроку брать объект в руки.

Результат:
значение из перечня

*   Varwin.InteractionBehaviour.GrabState.Enabled

*   Varwin.InteractionBehaviour.GrabState.Disabled

**Пример:**

result = instance.InteractionBehaviour.CanGrab

########## _generated_Varwin_ListUtils.html.md
Title: ListUtils — документация Varwin 18

_class_ Varwin.ListUtils[]

Предоставляет функции для работы со списками.

_static_ FirstIndex(_list:List[Any]_, _item:Any_)→Any[]
Возвращает индекс первого вхождения первого текста во второй текст. Возвращает 0, если текст не найден.

**Пример:**

result = Varwin.ListUtils.FirstIndex([sceneObject, Varwin.Vector3(1,1,1)], "test")

_static_ LastIndex(_list:List[Any]_, _item:Any_)→Any[]
Возвращает индекс последнего вхождения первого текста во второй текст. Возвращает 0, если текст не найден.

**Пример:**

result = Varwin.ListUtils.LastIndex([sceneObject, Varwin.Vector3(1,1,1)], "test")

########## _generated_Varwin_Math.html.md

# Math[]

_class_ Varwin.Math[]

Предоставляет функции для работы с числами.

_static_ IsPrime(_number:int_)→bool[]
Возвращает true, если число является простым.

**Пример:**

result = Varwin.Math.IsPrime(0)

########## _generated_Varwin_Method.html.md

# Method[]

_class_ Varwin.Method[]

########## _generated_Varwin_MotionBehaviour.html.md
Title: MotionBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.MotionBehaviour[]

_class_ Axis[]

X _:Any_ _=Ellipsis_[]Y _:Any_ _=Ellipsis_[]Z _:Any_ _=Ellipsis_[]_class_ LockRotationRules[]

Lock _:Any_ _=Ellipsis_[]OnlyHorizontal _:Any_ _=Ellipsis_[]AllowAll _:Any_ _=Ellipsis_[]TeleportTo(_target:[Object]_)→None[]
Мгновенно перемещает указанный объект по координатам второго объекта.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

instance.MotionBehaviour.TeleportTo(sceneObject1)

SetPosition(_targetPosition:[Vector3]_)→None[]
Мгновенно перемещает указанный объект в позицию, заданную с помощью координат в мировом пространстве.

**Пример:**

instance.MotionBehaviour.SetPosition(Varwin.Vector3(1,0,0))

MoveByAxisWithSpeed(_axis:[Vector3]_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта в направлении выбранной оси с заданной скоростью. Перемещение продолжается, пока оно не будет остановлено блоком завершения перемещения. Чтобы изменить направление перемещения, используйте отрицательные значение скорости.

**Пример:**

instance.MotionBehaviour.MoveByAxisWithSpeed(Varwin.Vector3(1,0,0), 0)

_async_ MoveByAxisAtDistance(_axis:[Vector3]_, _distance:float_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта в направлении выбранной оси на заданное расстояние с заданной скоростью. Перемещение продолжается, пока объект не преодолеет расстояние. Чтобы изменить направление перемещения, используйте отрицательные значение скорости.

**Пример:**

await instance.MotionBehaviour.MoveByAxisAtDistance(Varwin.Vector3(1,0,0), 0, 0)

_async_ MoveByAxisOverTime(_axis:[Vector3]_, _duration:float_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта в направлении выбранной оси в течение указанного времени с заданной скоростью. Перемещение продолжается, пока не истечет время. Чтобы изменить направление перемещения, используйте отрицательные значение скорости.

**Пример:**

await instance.MotionBehaviour.MoveByAxisOverTime(Varwin.Vector3(1,0,0), 0, 0)

_async_ MoveToObjectAtSpeed(_target:[Object]_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта в направлении второго объекта с заданной скоростью. Перемещение продолжается, пока указанный объект не достигнет второго объекта.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

await instance.MotionBehaviour.MoveToObjectAtSpeed(sceneObject1, 0)

_async_ MoveToCoordinatesAtSpeed(_target:[Vector3]_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта в направлении указанных координат с заданной скоростью. Перемещение продолжается, пока объект не достигнет координат.

**Пример:**

await instance.MotionBehaviour.MoveToCoordinatesAtSpeed(Varwin.Vector3(1,0,0), 0)

_async_ MoveAlongThePath(_path:List[[Object]|[Vector3]]_, _speed:float_)→None[]
Запускает процесс перемещения указанного объекта по маршруту с указанной скоростью. Маршрут представляет собой список объектов или координат в мировом пространстве, заданных векторами.

**Пример:**

await instance.MotionBehaviour.MoveAlongThePath("test", 0)

Stop()→None[]
Управляет любым перемещением. Приостановленное движение можно возобновить блоком “Продолжить”.

**Пример:**

instance.MotionBehaviour.Stop()

Pause()→None[]
Управляет любым перемещением. Приостановленное движение можно возобновить блоком “Продолжить”.

**Пример:**

instance.MotionBehaviour.Pause()

Continue()→None[]
Управляет любым перемещением. Приостановленное движение можно возобновить блоком “Продолжить”.

**Пример:**

instance.MotionBehaviour.Continue()

IsMovingNow()→bool[]
Возвращает “истину”, если указанный объект перемещается в данный момент. В противном случае возвращает “ложь”.

**Пример:**

result = instance.MotionBehaviour.IsMovingNow()

GetDistanceToObject(_target:[Object]_)→float[]
Возвращает расстояние по прямой от указанного объекта до второго объекта. Расстояние возвращается в метрах в виде вещественного числа.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

result = instance.MotionBehaviour.GetDistanceToObject(sceneObject1)

GetDistanceToVector(_target:[Vector3]_)→float[]
Возвращает расстояние по прямой от указанного объекта до мировых координат, указанных с помощью вектора. Расстояние возвращается в метрах в виде вещественного числа.

**Пример:**

result = instance.MotionBehaviour.GetDistanceToVector(Varwin.Vector3(1,0,0))

_property_ Position _:[Vector3]_[]
Возвращает позицию указанного объекта в мировых координатах в виде вектора [x; y; z]

**Пример:**

result = instance.MotionBehaviour.Position

_property_ PositionX _:float_[]
Возвращает позицию указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.MotionBehaviour.PositionX

_property_ PositionY _:float_[]
Возвращает позицию указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.MotionBehaviour.PositionY

_property_ PositionZ _:float_[]
Возвращает позицию указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.MotionBehaviour.PositionZ

_property_ MovementFaceDirection _:[Vector3]_[]
Задает сторону объекта, которой он будет направлен в сторону перемещения. Значение для настройки перемещения объекта “вперёд лицом”: (x: 0; y: 0; z: 1)

**Пример:**

result = instance.MotionBehaviour.MovementFaceDirection

_property_ MinimumTargetStopDistance _:float_[]
Задает минимальное расстояние между заданным и целевым объектами, чтобы движение к нему считалось завершенным. Вычисляется расстояние между центрами объектов, поэтому использование значения 0 не рекомендуется.

**Пример:**

result = instance.MotionBehaviour.MinimumTargetStopDistance

AddMovementFinishedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект завершает любое перемещение. Перемещение считается завершенным, если объект достиг целевой позиции, или если перемещение было остановлено соответствующим блоком. В параметр передается объект, для которого сработало событие.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnMovementFinished(sender):
  ...
instance.MotionBehaviour.AddMovementFinishedHandler(OnMovementFinished)

AddToWrapperMovementFinishedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект завершает перемещение к целевому объекту. В параметры передается объект, у которого сработало событие (перемещающийся объект), а также объект, к которому было завершено перемещение (целевой объект).

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Object): целевой объект

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnToWrapperMovementFinished(target, sender):
  ...
instance.MotionBehaviour.AddToWrapperMovementFinishedHandler(OnToWrapperMovementFinished)

AddToVectorMovementFinishedHandler(_handler:Callable[[[Vector3],[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект завершает перемещение к целевым координатам. В параметры передается объект, у которого сработало событие (перемещающийся объект), а также координаты, в виде вектора, к которым было завершено перемещение (целевые координаты).

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Vector3): целевые координаты

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnToVectorMovementFinished(target, sender):
  ...
instance.MotionBehaviour.AddToVectorMovementFinishedHandler(OnToVectorMovementFinished)

AddWaypointReachedHandler(_handler:Callable[[int,Any,[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект, двигающийся по маршруту, достигает очередную точки маршрута. В параметры передается объект, у которого сработало событие, номер точки в маршруте, а также достигнутая точка.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   wayPointIndex (int): номер точки в маршруте

*   waypoint (Any): достигнутая точка

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnWaypointReached(wayPointIndex, waypoint, sender):
  ...
instance.MotionBehaviour.AddWaypointReachedHandler(OnWaypointReached)

########## _generated_Varwin_Object.html.md
Title: Object — документация Varwin 18

_class_ Varwin.Object[]

Представление объекта сцены.

_property_ InteractionBehaviour _:[InteractionBehaviour]_[]
Получает информацию о поведении объекта при взаимодействии.

**Пример:**

result = instance.InteractionBehaviour

_property_ MotionBehaviour _:[MotionBehaviour]_[]
Получает поведение движения объекта.

**Пример:**

result = instance.MotionBehaviour

_property_ PhysicsBehaviour _:[PhysicsBehaviour]_[]
Получает физическое поведение объекта.

**Пример:**

result = instance.PhysicsBehaviour

_property_ RotateBehaviour _:[RotateBehaviour]_[]
Определяет поведение объекта при повороте.

**Пример:**

result = instance.RotateBehaviour

_property_ ScaleBehaviour _:[ScaleBehaviour]_[]
Получает поведение объекта при масштабировании.

**Пример:**

result = instance.ScaleBehaviour

_property_ VisualizationBehaviour _:[VisualizationBehaviour]_[]
Возвращает поведение объекта при визуализации.

**Пример:**

result = instance.VisualizationBehaviour

_property_ Activity _:bool_[]
Получает активное состояние объекта.

**Пример:**

result = instance.Activity

_property_ Enabled _:bool_[]
Возвращает включенное состояние объекта.

**Пример:**

result = instance.Enabled

GetName()→str[]
Получает имя объекта.

**Пример:**

result = instance.GetName()

GetTypeName()→str[]
Возвращает тип объекта.

**Пример:**

result = instance.GetTypeName()

GetParent()→[Object][]
Возвращает родительский объект.

Результат:
объект сцены

**Пример:**

result = instance.GetParent()

GetChildren()→List[[Object]][]
Получает список дочерних объектов.

**Пример:**

result = instance.GetChildren()

GetDescendants()→List[[Object]][]
Получает список всех объектов-потомков (детей, внуков и т. д.).

**Пример:**

result = instance.GetDescendants()

GetAncestry()→List[[Object]][]
Получает список объектов-предков (родителей, бабушек и дедушек и т. д.).

**Пример:**

result = instance.GetAncestry()

Enable()→None[]
Включает объект.

**Пример:**

instance.Enable()

Disable()→None[]
Отключает объект.

**Пример:**

instance.Disable()

Activate()→None[]
Активируйте объект.

**Пример:**

instance.Activate()

Deactivate()→None[]
Деактивировать объект.

**Пример:**

instance.Deactivate()

IsActive()→bool[]
Проверяет, активен ли объект.

**Пример:**

result = instance.IsActive()

IsInactive()→bool[]
Проверяет, является ли объект неактивным.

**Пример:**

result = instance.IsInactive()

IsEnabled()→bool[]
Проверяет, включен ли объект.

**Пример:**

result = instance.IsEnabled()

IsDisabled()→bool[]
Проверяет, отключен ли объект.

**Пример:**

result = instance.IsDisabled()

TransformPoint(_vector:[Vector3]_)→[Vector3][]
Преобразует точку из локального пространства в мировое.

**Пример:**

result = instance.TransformPoint(Varwin.Vector3(1,0,0))

InverseTransformPoint(_vector:[Vector3]_)→[Vector3][]
Преобразует точку из мирового пространства в локальное.

**Пример:**

result = instance.InverseTransformPoint(Varwin.Vector3(1,0,0))

########## _generated_Varwin_Objects.html.md
Title: Objects — документация Varwin 18

_class_ Varwin.Objects[]

Предоставляет возможность работы с объектами сцены.

_static_ GetAll()→List[[Object]][]
Возвращает все объекты на сцене.

**Пример:**

result = Varwin.Objects.GetAll()

T _=~T_[]_static_ GetObjectsOfType(_type:Type[T]_)→List[T][]
Возвращает все объекты сцены указанного типа.

**Пример:**

result = Varwin.Objects.GetObjectsOfType(PlayerWrapper)

_static_ GetObjectByInstanceId(_id:int_)→[Object][]
Возвращает объект сцены с указанным идентификатором.

Результат:
объект сцены

**Пример:**

result = Varwin.Objects.GetObjectByInstanceId(0)

_static_ GetObjectByVarName(_name:str_)→[Object][]
Возвращает объект сцены с указанным именем переменной.

Результат:
объект сцены

**Пример:**

result = Varwin.Objects.GetObjectByVarName("text")

########## _generated_Varwin_PhysicsBehaviour.html.md
Title: PhysicsBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.PhysicsBehaviour[]

_class_ Relativeness[]

Self _:Any_ _=Ellipsis_[]World _:Any_ _=Ellipsis_[]_class_ GravityState[]

On _:Any_ _=Ellipsis_[]Off _:Any_ _=Ellipsis_[]_class_ KinematicState[]

Kinematic _:Any_ _=Ellipsis_[]NonKinematic _:Any_ _=Ellipsis_[]_class_ ObstacleState[]

Obstacle _:Any_ _=Ellipsis_[]NonObstacle _:Any_ _=Ellipsis_[]ApplyForceInDirection(_force:float_, _direction:[Vector3]_, _relative:int_)→None[]
Мгновенно прикладывает силу к объекту в направлении заданного вектора в выбранной системе координат. Величина измеряется в кг*м/с.

Параметры:
**(****int****)** (_relative_) –

значение из перечня

*   Varwin.PhysicsBehaviour.Relativeness.Self (int)

*   Varwin.PhysicsBehaviour.Relativeness.World (int)

**Пример:**

instance.PhysicsBehaviour.ApplyForceInDirection(0, Varwin.Vector3(1,0,0), Varwin.PhysicsBehaviour.Relativeness.Self)

_async_ StartApplyingForceInDirectionRelativeTo(_force:float_, _direction:[Vector3]_, _duration:float_, _relative:int_)→None[]
Прикладывает силу к объекту в направлении заданного вектора в выбранной системе координат в течение указанного времени. Величина измеряется в кг*м/с.

Параметры:
**(****int****)** (_relative_) –

значение из перечня

*   Varwin.PhysicsBehaviour.Relativeness.Self (int)

*   Varwin.PhysicsBehaviour.Relativeness.World (int)

**Пример:**

await instance.PhysicsBehaviour.StartApplyingForceInDirectionRelativeTo(0, Varwin.Vector3(1,0,0), 0, Varwin.PhysicsBehaviour.Relativeness.Self)

Pause()→None[]
Управляет действием любой силы на объект. Приостановленное действие силы можно возобновить блоком “Продолжить”.

**Пример:**

instance.PhysicsBehaviour.Pause()

Continue()→None[]
Управляет действием любой силы на объект. Приостановленное действие силы можно возобновить блоком “Продолжить”.

**Пример:**

instance.PhysicsBehaviour.Continue()

Stop()→None[]
Управляет действием любой силы на объект. Приостановленное действие силы можно возобновить блоком “Продолжить”.

**Пример:**

instance.PhysicsBehaviour.Stop()

_property_ Mass _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.Mass

_property_ Bounciness _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.Bounciness

_property_ Gravity _:int_[]
Задает, воздействует ли гравитация на объект.

**Пример:**

result = instance.PhysicsBehaviour.Gravity

_property_ LinearDrag _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.LinearDrag

_property_ AngularDrag _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.AngularDrag

_property_ Acceleration _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.Acceleration

_property_ Speed _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.Speed

_property_ AngularSpeed _:float_[]
Возвращает величину выбранного физического свойства объекта.

**Пример:**

result = instance.PhysicsBehaviour.AngularSpeed

_property_ Kinematic _:int_[]
Задает статичность указанного объекта. Если объект статичный, никакие физические силы не воздействуют на него.

Результат:
значение из перечня

*   Varwin.PhysicsBehaviour.KinematicState.Kinematic

*   Varwin.PhysicsBehaviour.KinematicState.NonKinematic

**Пример:**

result = instance.PhysicsBehaviour.Kinematic

_property_ Obstacle _:int_[]
Задает, является ли указанный объект препятствием для игрока и других объектов.

Результат:
значение из перечня

*   Varwin.PhysicsBehaviour.ObstacleState.Obstacle

*   Varwin.PhysicsBehaviour.ObstacleState.NonObstacle

**Пример:**

result = instance.PhysicsBehaviour.Obstacle

IsAffectedByForceNow()→bool[]
Возвращает “истину”, если сила действует на указанный объект в данный момент. В противном случае возвращает “ложь”

**Пример:**

result = instance.PhysicsBehaviour.IsAffectedByForceNow()

AddApplicationOfForceCompletedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда сила перестает действовать на указанный объект. В параметр передается объект, для которого сработало событие.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnApplicationOfForceCompleted(sender):
  ...
instance.PhysicsBehaviour.AddApplicationOfForceCompletedHandler(OnApplicationOfForceCompleted)

########## _generated_Varwin_Project.html.md
Title: Project — документация Varwin 18

_class_ Varwin.Project[]

Предоставляет возможность управления состоянием логики.

_static_ RestartScene()→None[]
Restarts the current scene.

**Пример:**

Varwin.Project.RestartScene()

_static_ LoadSceneByGuid(_guid:str_)→None[]
Loads the scene with the specified identifier.

**Пример:**

Varwin.Project.LoadSceneByGuid("text")

_static_ LoadSceneByName(_name:str_)→None[]
Loads the scene with the specified name.

**Пример:**

Varwin.Project.LoadSceneByName("text")

_static_ LoadConfigurationByGuid(_guid:str_)→None[]
Loads the configuration with the specified identifier.

**Пример:**

Varwin.Project.LoadConfigurationByGuid("text")

_static_ LoadConfigurationByName(_name:str_)→None[]
Loads the configuration with the specified name.

**Пример:**

Varwin.Project.LoadConfigurationByName("text")

_static_ AddPlatformChangedToVRHandler(_handler:Callable[,CoroutineType]_)→None[]
Добавляет функцию-обработчик, которая вызывается при смене платформы на VR.

Параметры:
**handler** – Асинхронная функция-обработчик

**Пример:**

async def OnPlatformChangedToVR():
  ...
Varwin.Project.AddPlatformChangedToVRHandler(OnPlatformChangedToVR)

_static_ AddPlatformChangedToARHandler(_handler:Callable[,CoroutineType]_)→None[]
Добавляет функцию-обработчик, которая будет вызываться при смене платформы на AR.

Параметры:
**handler** – Асинхронная функция-обработчик

**Пример:**

async def OnPlatformChangedToAR():
  ...
Varwin.Project.AddPlatformChangedToARHandler(OnPlatformChangedToAR)

_static_ AddPlatformChangedToDesktopHandler(_handler:Callable[,CoroutineType]_)→None[]
Добавляет функцию-обработчик, которая вызывается при смене платформы на ПК.

Параметры:
**handler** – Асинхронная функция-обработчик

**Пример:**

async def OnPlatformChangedToDesktop():
  ...
Varwin.Project.AddPlatformChangedToDesktopHandler(OnPlatformChangedToDesktop)

_static_ AddPlatformChangedToNettleDeskHandler(_handler:Callable[,CoroutineType]_)→None[]
Добавляет функцию-обработчик, которая будет вызываться при смене платформы на NettleDesk.

Параметры:
**handler** – Асинхронная функция-обработчик

**Пример:**

async def OnPlatformChangedToNettleDesk():
  ...
Varwin.Project.AddPlatformChangedToNettleDeskHandler(OnPlatformChangedToNettleDesk)

_static_ AddPrepareSceneHandler(_handler:Callable[,CoroutineType]_)→None[]
Добавляет функцию-обработчик, вызываемую во время подготовки сцены.

Параметры:
**handler** – Асинхронная функция-обработчик

**Пример:**

async def OnPrepareScene():
  ...
Varwin.Project.AddPrepareSceneHandler(OnPrepareScene)

########## _generated_Varwin_Property.html.md

# Property[]

_class_ Varwin.Property[]

########## _generated_Varwin_Random.html.md
Title: Random — документация Varwin 18

_class_ Varwin.Random[]

Предоставляет методы расширения для работы со случайными числами.

_static_ TrueWithProbability(_value:float_)→bool[]
Возвращает True с заданной вероятностью, в противном случае False.

**Пример:**

result = Varwin.Random.TrueWithProbability(0)

_static_ RandInt(_a:int_, _b:int_)→int[]
Returns an integer in the specified range

**Пример:**

result = Varwin.Random.RandInt(0, 0)

_static_ RandFloat(_a:float_, _b:float_)→float[]
Returns a real number in the specified range

**Пример:**

result = Varwin.Random.RandFloat(0, 0)

########## _generated_Varwin_Range.html.md

# Range[]

_class_ Varwin.Range(_start:float_, _stop:float_, _step:float_)[]

Диапазонный тип представляет собой неизменяемую последовательность чисел и обычно используется для выполнения определенного количества циклов for.

########## _generated_Varwin_Requests.html.md
Title: Requests — документация Varwin 18

[Varwin]_class_ Varwin.Requests[]

Provides HTTP client functionality.

_class_ Request[]

HTTP request object.

_class_ Response[]

HTTP response object.

status_code _:int_[]text _:Any_[]content _:Any_[]_async static_ Get(_url:str_, _*_, _params:Dict[str,str]|List[Tuple[str,str]]|None=None_, _headers:Dict[str,str]|None=None_)→[Response][]
Send a GET request.

**Пример:**

response = await Varwin.Requests.Get("https://varwin.com")

_async static_ Post(_url:str_, _*_, _data:str|None=None_, _json:Any|None=None_, _headers:Dict[str,str]|None=None_)→[Response][]
Send a POST request.

**Пример:**

response = await Varwin.Requests.Post("https://varwin.com")

_async static_ Put(_url:str_, _*_, _data:str|None=None_, _json:Any|None=None_, _headers:Dict[str,str]|None=None_)→[Response][]
Send a PUT request.

**Пример:**

response = await Varwin.Requests.Put("https://varwin.com")

_async static_ Delete(_url:str_, _*_, _data:str|None=None_, _json:Any|None=None_, _headers:Dict[str,str]|None=None_)→[Response][]
Send a DELETE request.

**Пример:**

response = await Varwin.Requests.Delete("https://varwin.com")

########## _generated_Varwin_RotateBehaviour.html.md
Title: RotateBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.RotateBehaviour[]

_class_ Axis[]

X _:Any_ _=Ellipsis_[]Y _:Any_ _=Ellipsis_[]Z _:Any_ _=Ellipsis_[]_class_ RotationAxis[]

All _:Any_ _=Ellipsis_[]LocalX _:Any_ _=Ellipsis_[]LocalY _:Any_ _=Ellipsis_[]SetRotation(_eulerAngles:[Vector3]_)→None[]
Мгновенно задает поворот указанного объекта в градусах по трем осям. Поворот считается относительно мировых координат.

**Пример:**

instance.RotateBehaviour.SetRotation(Varwin.Vector3(1,0,0))

RotateAroundAxis(_angle:float_, _axis:int_)→None[]
Мгновенно поворачивает объект на указанный угол по выбранной оси.

Параметры:
**(****int****)** (_axis_) –

значение из перечня

*   Varwin.RotateBehaviour.Axis.X (int)

*   Varwin.RotateBehaviour.Axis.Y (int)

*   Varwin.RotateBehaviour.Axis.Z (int)

**Пример:**

instance.RotateBehaviour.RotateAroundAxis(0, Varwin.RotateBehaviour.Axis.X)

RotateToObjectAroundAxis(_target:[Object]_, _axis:int_)→None[]
Мгновенно поворачивает объект к другому выбранному объекту.

Параметры:
*   **(****Object****)** (_target_) – объект сцены

*   **(****int****)** (_axis_) –

значение из перечня

    *   Varwin.RotateBehaviour.RotationAxis.All (int)

    *   Varwin.RotateBehaviour.RotationAxis.LocalX (int)

    *   Varwin.RotateBehaviour.RotationAxis.LocalY (int)

**Пример:**

instance.RotateBehaviour.RotateToObjectAroundAxis(sceneObject1, Varwin.RotateBehaviour.RotationAxis.All)

RotateAsObject(_target:[Object]_)→None[]
Мгновенно задает объекту параметры вращения другого выбранного объекта.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

instance.RotateBehaviour.RotateAsObject(sceneObject1)

RotateAroundAxisWithSpeed(_axis:int_, _speed:float_)→None[]
Запускает вращение указанного объекта вокруг выбранной локальной оси с заданной скоростью. Вращение происходит, пока оно не будет остановлено блоком остановки вращения. Чтобы изменить направление вращения, используйте отрицательные значения скорости.

Параметры:
**(****int****)** (_axis_) –

значение из перечня

*   Varwin.RotateBehaviour.Axis.X (int)

*   Varwin.RotateBehaviour.Axis.Y (int)

*   Varwin.RotateBehaviour.Axis.Z (int)

**Пример:**

instance.RotateBehaviour.RotateAroundAxisWithSpeed(Varwin.RotateBehaviour.Axis.X, 0)

_async_ RotationAroundAxisWithSpeedOverTime(_axis:int_, _time:float_, _speed:float_)→None[]
Запускает вращение объекта вокруг выбранной оси в течение указанного времени с заданной скоростью. Для изменения направления вращения используйте отрицательные значения скорости.

Параметры:
**(****int****)** (_axis_) –

значение из перечня

*   Varwin.RotateBehaviour.Axis.X (int)

*   Varwin.RotateBehaviour.Axis.Y (int)

*   Varwin.RotateBehaviour.Axis.Z (int)

**Пример:**

await instance.RotateBehaviour.RotationAroundAxisWithSpeedOverTime(Varwin.RotateBehaviour.Axis.X, 0, 0)

RotateAroundAnotherObjectAxisWithSpeed(_axis:int_, _target:[Object]_, _speed:float_)→None[]
Запускает вращение объекта вокруг выбранной оси другого объекта с заданной скоростью.

Параметры:
*   **(****int****)** (_axis_) –

значение из перечня

    *   Varwin.RotateBehaviour.Axis.X (int)

    *   Varwin.RotateBehaviour.Axis.Y (int)

    *   Varwin.RotateBehaviour.Axis.Z (int)

*   **(****Object****)** (_target_) – объект сцены

**Пример:**

instance.RotateBehaviour.RotateAroundAnotherObjectAxisWithSpeed(Varwin.RotateBehaviour.Axis.X, sceneObject2, 0)

_async_ LookAtObjectWithSpeedAroundAxis(_target:[Object]_, _speed:float_, _axis:int_)→None[]
Запускает вращение объекта к другому выбранному объекту с указанной скоростью.

Параметры:
*   **(****Object****)** (_target_) – объект сцены

*   **(****int****)** (_axis_) –

значение из перечня

    *   Varwin.RotateBehaviour.RotationAxis.All (int)

    *   Varwin.RotateBehaviour.RotationAxis.LocalX (int)

    *   Varwin.RotateBehaviour.RotationAxis.LocalY (int)

**Пример:**

await instance.RotateBehaviour.LookAtObjectWithSpeedAroundAxis(sceneObject1, 0, Varwin.RotateBehaviour.RotationAxis.All)

_async_ RotateAsObjectWithSpeed(_target:[Object]_, _speed:float_)→None[]
Запускает вращение объекта в соответствии с параметрами другого выбранного объекта с указанной скоростью.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

await instance.RotateBehaviour.RotateAsObjectWithSpeed(sceneObject1, 0)

_async_ RotateToVectorWithSpeed(_target:[Vector3]_, _speed:float_)→None[]
Запускает вращение объекта к углу в мировых координатах, заданного вектором с углами по каждой из осей [0…360]. Поворот будет производится по наименьшему пути.

**Пример:**

await instance.RotateBehaviour.RotateToVectorWithSpeed(Varwin.Vector3(1,0,0), 0)

_async_ RotateAroundAxisByAngleWithSpeed(_axis:int_, _angle:float_, _speed:float_)→None[]
Запускает вращение объекта вокруг выбранной локальной оси с заданной скоростью. Для изменения направления вращения используйте отрицательные значения скорости.

Параметры:
**(****int****)** (_axis_) –

значение из перечня

*   Varwin.RotateBehaviour.Axis.X (int)

*   Varwin.RotateBehaviour.Axis.Y (int)

*   Varwin.RotateBehaviour.Axis.Z (int)

**Пример:**

await instance.RotateBehaviour.RotateAroundAxisByAngleWithSpeed(Varwin.RotateBehaviour.Axis.X, 0, 0)

Stop()→None[]
Управляет любым вращением. Приостановленное вращение можно возобновить блоком «Продолжить».

**Пример:**

instance.RotateBehaviour.Stop()

Pause()→None[]
Управляет любым вращением. Приостановленное вращение можно возобновить блоком «Продолжить».

**Пример:**

instance.RotateBehaviour.Pause()

Continue()→None[]
Управляет любым вращением. Приостановленное вращение можно возобновить блоком «Продолжить».

**Пример:**

instance.RotateBehaviour.Continue()

IsRotatingNow()→bool[]
Возвращает «истину», если указанный объект вращается в данный момент. В противном случае возвращает “ложь”

**Пример:**

result = instance.RotateBehaviour.IsRotatingNow()

GetRotationAroundAxisToObject(_axis:int_, _target:[Object]_)→float[]
Возвращает угол поворота объекта относительно другого объекта по выбранной оси.

Параметры:
*   **(****int****)** (_axis_) –

значение из перечня

    *   Varwin.RotateBehaviour.Axis.X (int)

    *   Varwin.RotateBehaviour.Axis.Y (int)

    *   Varwin.RotateBehaviour.Axis.Z (int)

*   **(****Object****)** (_target_) – объект сцены

**Пример:**

result = instance.RotateBehaviour.GetRotationAroundAxisToObject(Varwin.RotateBehaviour.Axis.X, sceneObject2)

GetRotationToObject(_target:[Object]_)→[Vector3][]
Возвращает поворот объекта относительно другого объекта в виде вектора.

Параметры:
**(****Object****)** (_target_) – объект сцены

**Пример:**

result = instance.RotateBehaviour.GetRotationToObject(sceneObject1)

AngleX()→float[]
Возвращает угол поворота указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.RotateBehaviour.AngleX()

AngleY()→float[]
Возвращает угол поворота указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.RotateBehaviour.AngleY()

AngleZ()→float[]
Возвращает угол поворота указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.RotateBehaviour.AngleZ()

_property_ Angle _:[Vector3]_[]
Возвращает поворот объекта в мировых координатах в виде вектора.

**Пример:**

result = instance.RotateBehaviour.Angle

AddRotationFinishedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект завершает любое вращение. Вращение считается завершенным, если объект достиг поворота к целевой точке, или если вращение было остановлено соответствующим блоком. В параметр передается объект, для которого сработало событие.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnRotationFinished(sender):
  ...
instance.RotateBehaviour.AddRotationFinishedHandler(OnRotationFinished)

AddToWrapperRotationFinishedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда объект завершил поворот к целевому объекту, либо когда повернулся так же, как целевой объект. В параметры передается объект, для которого сработало событие, а также объект, к которому был завершен поворот (целевой объект).

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Object): целевой объект

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnToWrapperRotationFinished(target, sender):
  ...
instance.RotateBehaviour.AddToWrapperRotationFinishedHandler(OnToWrapperRotationFinished)

AddAsWrapperRotationFinishedHandler(_handler:Callable[[[Object],[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда объект завершил поворот к целевому объекту, либо когда повернулся так же, как целевой объект. В параметры передается объект, для которого сработало событие, а также объект, к которому был завершен поворот (целевой объект).

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Object): целевой объект

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnAsWrapperRotationFinished(target, sender):
  ...
instance.RotateBehaviour.AddAsWrapperRotationFinishedHandler(OnAsWrapperRotationFinished)

AddToVectorRotationFinishedHandler(_handler:Callable[[[Vector3],[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда объект завершает поворот к целевому вращению. В параметры передается объект, для которого сработало событие (вращающийся объект), а также вращение, в виде вектора, к которому был завершен поворот (целевое вращение).

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   target (Vector3): целевой поворот

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnToVectorRotationFinished(target, sender):
  ...
instance.RotateBehaviour.AddToVectorRotationFinishedHandler(OnToVectorRotationFinished)

########## _generated_Varwin_ScaleBehaviour.html.md
Title: ScaleBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.ScaleBehaviour[]

SetScale(_targetScale:[Vector3]_)→None[]
Мгновенно задает масштаб указанного объекта.

**Пример:**

instance.ScaleBehaviour.SetScale(Varwin.Vector3(1,0,0))

_async_ ScaleOverTime(_target:[Vector3]_, _time:float_)→None[]
Масштабирует объект до заданных значений в течение указанного времени. Изменение происходит относительно текущего (на момент срабатывания блока) масштаба объекта.

**Пример:**

await instance.ScaleBehaviour.ScaleOverTime(Varwin.Vector3(1,0,0), 0)

_async_ ScaleByFactorOverTime(_target:float_, _time:float_)→None[]
Масштабирует объект в заданное количество раз в течение указанного времени. Изменение происходит относительно текущего (на момент срабатывания блока) масштаба объекта.

**Пример:**

await instance.ScaleBehaviour.ScaleByFactorOverTime(0, 0)

Stop()→None[]
Управляет любым масштабированием. Приостановленное масштабирование можно возобновить блоком “Продолжить”.

**Пример:**

instance.ScaleBehaviour.Stop()

Pause()→None[]
Управляет любым масштабированием. Приостановленное масштабирование можно возобновить блоком “Продолжить”.

**Пример:**

instance.ScaleBehaviour.Pause()

Continue()→None[]
Управляет любым масштабированием. Приостановленное масштабирование можно возобновить блоком “Продолжить”.

**Пример:**

instance.ScaleBehaviour.Continue()

IsScalingNow()→bool[]
Возвращает “истину”, если объект масштабируется в данный момент. В противном случае возвращает “ложь”.

**Пример:**

result = instance.ScaleBehaviour.IsScalingNow()

_property_ Scale _:[Vector3]_[]
Возвращает масштаб указанного объекта в мировых координатах в виде вектора.

**Пример:**

result = instance.ScaleBehaviour.Scale

_property_ ScaleX _:float_[]
Возвращает масштаб указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.ScaleBehaviour.ScaleX

_property_ ScaleY _:float_[]
Возвращает масштаб указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.ScaleBehaviour.ScaleY

_property_ ScaleZ _:float_[]
Возвращает масштаб указанного объекта по выбранной оси в мировых координатах.

**Пример:**

result = instance.ScaleBehaviour.ScaleZ

AddScalingFinishedHandler(_handler:Callable[[[Object]],CoroutineType]_)→None[]
Событие срабатывает, когда указанный объект завершает любое масштабирование. Вращение считается завершенным, если объект достиг целевого масштаба, или если масштабирование было остановлено соответствующим блоком. В параметр передается объект, для которого сработало событие.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   sender (Object): объект, который вызвал событие

**Пример:**

async def OnScalingFinished(sender):
  ...
instance.ScaleBehaviour.AddScalingFinishedHandler(OnScalingFinished)

########## _generated_Varwin_StringUtils.html.md
Title: StringUtils — документация Varwin 18

_class_ Varwin.StringUtils[]

Предоставляет методы расширения для работы со строками.

_static_ GetLineBreak()→str[]
Получает соответствующую строку разрыва строки для указанной платформы.

**Пример:**

result = Varwin.StringUtils.GetLineBreak()

_static_ Replace(_source:str_, _oldSubstring:str_, _newSubstring:str_)→str[]
Заменяет вхождения подстроки в строке.

**Пример:**

result = Varwin.StringUtils.Replace("text", "text", "text")

_static_ GetRandomLetter(_source:str_)→str[]
Возвращает случайную букву из строки.

**Пример:**

result = Varwin.StringUtils.GetRandomLetter("text")

########## _generated_Varwin_UserType.html.md

# UserType[]

_class_ Varwin.UserType[]

Тип данных, определяемый пользователем.

########## _generated_Varwin_Variable.html.md
Title: Variable — документация Varwin 18

_class_ Varwin.Variable[]

Представляет переменную, которая может инициировать события при изменении ее значения.

_property_ Value _:Any_[]
Получает текущее значение переменной.

**Пример:**

result = instance.Value

AddValueChangedHandler(_handler:Callable[[Any,Any],CoroutineType]_)→None[]
Добавляет функцию-обработчик, которая вызывается при изменении значения переменной.

Параметры:
**handler** –

Асинхронная функция-обработчик с сигнатурой:

*   oldValue (Any)

*   newValue (Any)

**Пример:**

async def OnValueChanged(oldValue, newValue):
  ...
instance.AddValueChangedHandler(OnValueChanged)

########## _generated_Varwin_Vector3.html.md
Title: Vector3 — документация Varwin 18

[Varwin]_class_ Varwin.Vector3[]_class_ Varwin.Vector3(_x:float_, _y:float_, _z:float_)

Представляет собой трехмерный вектор.

X _:float_[]Y _:float_[]Z _:float_[]_static_ Dot(_left:[Vector3]_, _right:[Vector3]_)→[Vector3][]
Вычисляет скалярное произведение двух векторов

**Пример:**

result = Varwin.Vector3.Dot(Varwin.Vector3(1,0,0), Varwin.Vector3(1,0,0))

_static_ Cross(_left:[Vector3]_, _right:[Vector3]_)→[Vector3][]
Вычисляет векторное произведение двух векторов.

**Пример:**

result = Varwin.Vector3.Cross(Varwin.Vector3(1,0,0), Varwin.Vector3(1,0,0))

_static_ Distance(_left:[Vector3]_, _right:[Vector3]_)→float[]
Вычисляет расстояние между двумя векторами.

**Пример:**

result = Varwin.Vector3.Distance(Varwin.Vector3(1,0,0), Varwin.Vector3(1,0,0))

_static_ Rotate(_vector:[Vector3]_, _eulerAngles:[Vector3]_)→[Vector3][]
Поворачивает вектор вокруг указанной оси на заданный угол (в углах Эйлера).

**Пример:**

result = Varwin.Vector3.Rotate(Varwin.Vector3(1,0,0), Varwin.Vector3(1,0,0))

_property_ Normalized _:[Vector3]_[]
Возвращает нормализованную версию вектора (единичный вектор).

**Пример:**

result = instance.Normalized

_property_ Magnitude _:float_[]
Получает величину (длину) вектора.

**Пример:**

result = instance.Magnitude

########## _generated_Varwin_VisualizationBehaviour.html.md
Title: VisualizationBehaviour — документация Varwin 18

[Varwin]_class_ Varwin.VisualizationBehaviour[]

_class_ PlayableState[]

Stop _:Any_ _=Ellipsis_[]Pause _:Any_ _=Ellipsis_[]Continue _:Any_ _=Ellipsis_[]_class_ ShadowCastingMode[]

Off _:Any_ _=Ellipsis_[]On _:Any_ _=Ellipsis_[]TwoSided _:Any_ _=Ellipsis_[]ShadowsOnly _:Any_ _=Ellipsis_[]ChangeObjectColor(_color:[Color]_)→None[]
Мгновенно меняет цвет объекта на выбранный. При использовании блока с объектом, имеющим текстуры, блок придаст ему выбранный оттенок.

**Пример:**

instance.VisualizationBehaviour.ChangeObjectColor(Varwin.Color(1,1,0,1))

_async_ ChangeColorOverTime(_color:[Color]_, _time:float_)→None[]
Запускает изменение цвета объекта на выбранный в течение заданного времени. При использовании блока с объектом, имеющим текстуры, блок придаст ему выбранный оттенок.

**Пример:**

await instance.VisualizationBehaviour.ChangeColorOverTime(Varwin.Color(1,1,0,1), 0)

SetChangingColorState(_state:int_)→None[]
Управляет любым изменением цвета. Приостановленное изменение цвета можно продолжить соответствующим блоком.

Параметры:
**(****int****)** (_state_) –

значение из перечня

*   Varwin.VisualizationBehaviour.PlayableState.Stop (int)

*   Varwin.VisualizationBehaviour.PlayableState.Pause (int)

*   Varwin.VisualizationBehaviour.PlayableState.Continue (int)

**Пример:**

instance.VisualizationBehaviour.SetChangingColorState(Varwin.VisualizationBehaviour.PlayableState.Stop)

IsColorChangingNow()→bool[]
Возвращает “истину”, если указанный объект изменяет цвет в данный момент. В противном случае возвращает “ложь”.

**Пример:**

result = instance.VisualizationBehaviour.IsColorChangingNow()

_property_ Color _:[Color]_[]
Возвращает цвет указанного объекта в виде блока цвета.

**Пример:**

result = instance.VisualizationBehaviour.Color

########## _generated_Varwin_WaitForEndOfFrame.html.md

# WaitForEndOfFrame[]

_class_ Varwin.WaitForEndOfFrame[]

Асинхронно ожидает конца текущего кадра. Это предназначено для использования с циклом async for и может быть интегрировано с различными механизмами рендеринга или игрового цикла.

########## _generated_Varwin_WaitForSeconds.html.md

# WaitForSeconds[]

_class_ Varwin.WaitForSeconds(_seconds:float_)[]

Ожидает указанное количество секунд, используя асинхронный итератор. Это позволяет интегрировать ожидание в асинхронный цикл for и потенциально прерывать его.

########## _generated_Varwin_WaitWhile.html.md

# WaitWhile[]

_class_ Varwin.WaitWhile(_function:Callable[,bool]_)[]

Ожидает, пока заданное условие не станет ложным, используя асинхронный итератор. Это позволяет интегрировать ожидание в асинхронный цикл for и потенциально прерывать его.

########## _generated_Woodenoldtable_WoodenoldtableWrapper.html.md

# WoodenoldtableWrapper[]

_class_ Woodenoldtable.WoodenoldtableWrapper(_object:[Object]_)[]
Базовые классы: [`Object`]

########## genindex.html.md
Title: Алфавитный указатель — документация Varwin 18

[Varwin]

*   [Структура проекта]
*   [Асинхронное программирование]
*   [Отправка запросов]
*   [Примеры использования]
*   [API]
*   [Основная документация]

[Varwin]

*   
*   Алфавитный указатель

# Алфавитный указатель

[**A**] | [**B**] | [**C**] | [**D**] | [**E**] | [**F**] | [**G**] | [**H**] | [**I**] | [**J**] | [**K**] | [**L**] | [**M**] | [**N**] | [**O**] | [**P**] | [**R**] | [**S**] | [**T**] | [**U**] | [**V**] | [**W**] | [**X**] | [**Y**] | [**Z**]

## A

*   [A (атрибут Varwin.Color)]
*   [Acceleration (свойство Varwin.PhysicsBehaviour)]
*   [Activate() (метод Varwin.Object)]
*   [Activity (свойство Varwin.Object)]
*   [AddAnimationFinishedHandler() (метод VarwinModel.VarwinModelWrapper)]
*   [AddAnimationPausedHandler() (метод VarwinModel.VarwinModelWrapper)]
*   [AddAnimationStoppedHandler() (метод VarwinModel.VarwinModelWrapper)]
*   [AddAnyHandCollidedHandler() (метод Player.PlayerWrapper)]
*   [AddApplicationOfForceCompletedHandler() (метод Varwin.PhysicsBehaviour)]
*   [AddAsWrapperRotationFinishedHandler() (метод Varwin.RotateBehaviour)]
*   [AddBlueButtonWasPressedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddBlueButtonWasReleasedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddBotPathPointReachedHandler() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [AddBotTargetReachedHandler() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [AddCloseButtonPressedHandler() (метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [AddCollisionEndHandler() (статический метод Varwin.Collisions)]
*   [AddCollisionStartHandler() (статический метод Varwin.Collisions)]
*   [AddCompletedHandler() (метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [AddControllerDisabledHandler() (метод Player.PlayerWrapper)]
*   [AddControllerEnabledHandler() (метод Player.PlayerWrapper)]
*   [AddGrabEndedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddGrabStartedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddGreenButtonWasPressedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddGreenButtonWasReleasedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddMovementFinishedHandler() (метод Varwin.MotionBehaviour)]
*   [AddObjectEnteredHandler() (метод CustomZone.CustomZoneWrapper)]
*   [AddObjectExitedHandler() (метод CustomZone.CustomZoneWrapper)]
*   [AddPanoramaImageLoadedHandler() (метод VPanorama.VPanoramaWrapper)]
    *   [(метод VPanorama180.VPanorama180Wrapper)]

*   [AddPanoramaImageUnloadedHandler() (метод VPanorama.VPanoramaWrapper)]
    *   [(метод VPanorama180.VPanorama180Wrapper)]

*   [AddPlatformChangedToARHandler() (статический метод Varwin.Project)]
*   [AddPlatformChangedToDesktopHandler() (статический метод Varwin.Project)]
*   [AddPlatformChangedToNettleDeskHandler() (статический метод Varwin.Project)]
*   [AddPlatformChangedToVRHandler() (статический метод Varwin.Project)]
*   [AddPlaybackCompletedHandler() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinAudio.VarwinAudioWrapper)]

*   [AddPrepareSceneHandler() (статический метод Varwin.Project)]
*   [AddPressedHandler() (метод TutorialButton.TutorialButtonWrapper)]
*   [AddRedButtonWasPressedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddRedButtonWasReleasedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddReleasedHandler() (метод TutorialButton.TutorialButtonWrapper)]*   [AddRingHitHandler() (метод Basketball_Hoop.Basketball_HoopWrapper)]
*   [AddRotationFinishedHandler() (метод Varwin.RotateBehaviour)]
*   [AddScalingFinishedHandler() (метод Varwin.ScaleBehaviour)]
*   [AddSpeechCompletedHandler() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [AddStart() (статический метод Varwin.Async)]
*   [AddTargetFoundHandler() (метод ARMarker.ARMarkerWrapper)]
*   [AddTargetLostHandler() (метод ARMarker.ARMarkerWrapper)]
*   [AddTouchEndedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddTouchStartedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddToVectorMovementFinishedHandler() (метод Varwin.MotionBehaviour)]
*   [AddToVectorRotationFinishedHandler() (метод Varwin.RotateBehaviour)]
*   [AddToWrapperMovementFinishedHandler() (метод Varwin.MotionBehaviour)]
*   [AddToWrapperRotationFinishedHandler() (метод Varwin.RotateBehaviour)]
*   [AddUpdate() (статический метод Varwin.Async)]
*   [AddUseEndedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddUseStartedHandler() (метод Varwin.InteractionBehaviour)]
*   [AddValueChangedHandler() (метод Varwin.Variable)]
*   [AddVideoLoadedHandler() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [AddWaypointReachedHandler() (метод Varwin.MotionBehaviour)]
*   [AddYellowButtonWasPressedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [AddYellowButtonWasReleasedHandler() (метод SKJoystick.SKJoystickWrapper)]
*   [All (атрибут Player.PlayerWrapper.MovementType)]
    *   [(атрибут Varwin.RotateBehaviour.RotationAxis)]

*   [AllowAll (атрибут Varwin.MotionBehaviour.LockRotationRules)]
*   [Allowed (атрибут Player.PlayerWrapper.AllowedStates)]
*   [AllowMovementEverywhere() (метод Player.PlayerWrapper)]
*   [AllowMovementOnlyTeleportArea() (метод Player.PlayerWrapper)]
*   [AllowMovementType() (метод Player.PlayerWrapper)]
*   [AlwaysDrawRay (свойство Player.PlayerWrapper)]
*   [Angle (свойство Varwin.RotateBehaviour)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]

*   [AngleX() (метод Varwin.RotateBehaviour)]
*   [AngleY() (метод Varwin.RotateBehaviour)]
*   [AngleZ() (метод Varwin.RotateBehaviour)]
*   [AngularDrag (свойство Varwin.PhysicsBehaviour)]
*   [AngularSpeed (свойство Varwin.PhysicsBehaviour)]
*   [AnimationPlaybackMode (свойство VarwinModel.VarwinModelWrapper)]
*   [AnimationSpeed (свойство VarwinModel.VarwinModelWrapper)]
*   [Application (класс в Varwin)]
*   [ApplyForceInDirection() (метод Varwin.PhysicsBehaviour)]
*   [ARMarkerWrapper (класс в ARMarker)]
*   [Async (класс в Varwin)]
*   [AttachCameraToObject() (метод Player.PlayerWrapper)]
*   [Automatic (атрибут VBotBoy.VBotBoyWrapper.TextBubbleHideType)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.TextBubbleHideType)]

*   [AxisX (свойство SKJoystick.SKJoystickWrapper)]
*   [AxisY (свойство SKJoystick.SKJoystickWrapper)]

## B

*   [B (атрибут Varwin.Color)]
*   [Backward (атрибут VBotBoy.VBotBoyWrapper.MovementDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementDirection)]

*   [BadScript (атрибут TutorialDisplay.TutorialDisplayWrapper.Fonts)]
    *   [(атрибут VText.VTextWrapper.Fonts)]

*   [BallsBoxWrapper (класс в BallsBox)]
*   [Basketball_HoopWrapper (класс в Basketball_Hoop)]
*   [BasketballWrapper (класс в Basketball)]
*   [BeginColor (свойство Player.PlayerWrapper)]*   [BeginWidth (свойство Player.PlayerWrapper)]
*   [BlueButtonPressed() (метод SKJoystick.SKJoystickWrapper)]
*   [Bold (свойство VText.VTextWrapper)]
*   [BoldStyle (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [BothHands (атрибут Player.PlayerWrapper.PlayerHand)]
*   [Bottom (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentVerticalType)]
    *   [(атрибут VText.VTextWrapper.VerticalAlignment)]

*   [BottomPadding (свойство VText.VTextWrapper)]
*   [Bounciness (свойство Varwin.PhysicsBehaviour)]
*   [BoxColliderWrapper (класс в BoxCollider)]

## C

*   [CanGrab (свойство Varwin.InteractionBehaviour)]
*   [CanTeleport (свойство Varwin.InteractionBehaviour)]
*   [CanTouch (свойство Varwin.InteractionBehaviour)]
*   [CanUse (свойство Varwin.InteractionBehaviour)]
*   [CapsuleColliderWrapper (класс в CapsuleCollider)]
*   [Center (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentHorizontalType)]
    *   [(атрибут VText.VTextWrapper.HorizontalAlignment)]

*   [ChangeColorOverTime() (метод Varwin.VisualizationBehaviour)]
*   [ChangeObjectColor() (метод Varwin.VisualizationBehaviour)]
*   [CheckHoldAnyObject() (метод Player.PlayerWrapper)]
*   [CheckObjectInAnyHand() (метод Player.PlayerWrapper)]
*   [CheckObjectInLeftHand() (метод Player.PlayerWrapper)]
*   [CheckObjectInRightHand() (метод Player.PlayerWrapper)]
*   [Clockwise (атрибут VBotBoy.VBotBoyWrapper.RotationDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.RotationDirection)]

*   [Clone() (статический метод Varwin.Cloning)]
*   [CloneAtObjectPosition() (статический метод Varwin.Cloning)]
*   [CloneAtPosition() (статический метод Varwin.Cloning)]
*   [Cloning (класс в Varwin)]
*   [Collisions (класс в Varwin)]
*   [Color (класс в Varwin)]
    *   [(свойство TutorialBulb.TutorialBulbWrapper)]
    *   [(свойство Varwin.VisualizationBehaviour)]
    *   [(свойство VDirectionalLight.VDirectionalLightWrapper)]
    *   [(свойство VPointLight.VPointLightWrapper)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]*   [content (атрибут Varwin.Requests.Response)]
*   [Continue (атрибут Varwin.VisualizationBehaviour.PlayableState)]
*   [Continue() (метод Varwin.MotionBehaviour)]
    *   [(метод Varwin.PhysicsBehaviour)]
    *   [(метод Varwin.RotateBehaviour)]
    *   [(метод Varwin.ScaleBehaviour)]

*   [ContinuePath() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [Coroutine (класс в Varwin)]
*   [Counterclockwise (атрибут VBotBoy.VBotBoyWrapper.RotationDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.RotationDirection)]

*   [Cross() (статический метод Varwin.Vector3)]
*   [CurrentTime (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство VarwinAudio.VarwinAudioWrapper)]
    *   [(свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [CursorIsVisible (свойство Player.PlayerWrapper)]
*   [CustomZoneWrapper (класс в CustomZone)]

## D

*   [Deactivate() (метод Varwin.Object)]
*   [Debug (класс в Varwin)]
*   [DefaultSpawnPointWrapper (класс в DefaultSpawnPoint)]
*   [Delete() (статический метод Varwin.Requests)]
*   [Destroy() (статический метод Varwin.Cloning)]
*   [DestroyAllClones() (статический метод Varwin.Cloning)]
*   [DetachCameraFromObject() (метод Player.PlayerWrapper)]
*   [Direct (атрибут VarwinModel.VarwinModelWrapper.AnimationPlayTypeOptions)]
*   [Disable() (метод Varwin.Object)]
*   [Disabled (атрибут Player.PlayerWrapper.SwitchStateTypes)]
    *   [(атрибут Varwin.InteractionBehaviour.GrabState)]
    *   [(атрибут Varwin.InteractionBehaviour.TeleportState)]
    *   [(атрибут Varwin.InteractionBehaviour.TouchState)]
    *   [(атрибут Varwin.InteractionBehaviour.UseState)]*   [Distance() (статический метод Varwin.Vector3)]
*   [DontLock (атрибут StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper.PlayerLockOptions)]
    *   [(атрибут StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper.PlayerLockOptions)]
    *   [(атрибут VarwinVideo180.VarwinVideo180Wrapper.PlayerLockOptions)]
    *   [(атрибут VarwinVideo360.VarwinVideo360Wrapper.PlayerLockOptions)]
    *   [(атрибут VPanorama.VPanoramaWrapper.PlayerLockOptions)]
    *   [(атрибут VPanorama180.VPanorama180Wrapper.PlayerLockOptions)]

*   [Dot() (статический метод Varwin.Vector3)]
*   [DynamicModuleProvider (класс в Varwin)]
*   [DynamicValueDictionary (класс в Varwin)]

## E

*   [Enable() (метод Varwin.Object)]
*   [Enabled (атрибут Player.PlayerWrapper.SwitchStateTypes)]
    *   [(атрибут Varwin.InteractionBehaviour.GrabState)]
    *   [(атрибут Varwin.InteractionBehaviour.TeleportState)]
    *   [(атрибут Varwin.InteractionBehaviour.TouchState)]
    *   [(атрибут Varwin.InteractionBehaviour.UseState)]
    *   [(свойство Varwin.Object)]*   [EndColor (свойство Player.PlayerWrapper)]
*   [EndWidth (свойство Player.PlayerWrapper)]
*   [Enum (класс в Varwin)]
*   [Event (класс в Varwin)]

## F

*   [FirstIndex() (статический метод Varwin.ListUtils)]
*   [Flush (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentHorizontalType)]
    *   [(атрибут VText.VTextWrapper.HorizontalAlignment)]

*   [Font (свойство VText.VTextWrapper)]
*   [FontSizeMax (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [FontSizeMin (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [ForceDropFromBothHands() (метод Player.PlayerWrapper)]
*   [ForceDropObjectInLeftHand() (метод Player.PlayerWrapper)]*   [ForceDropObjectInRightHand() (метод Player.PlayerWrapper)]
*   [ForceGrabObjectInLeftHand() (метод Player.PlayerWrapper)]
*   [ForceGrabObjectInRightHand() (метод Player.PlayerWrapper)]
*   [Forward (атрибут VBotBoy.VBotBoyWrapper.MovementDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementDirection)]
    *   [(свойство SKHumanoidBot.SKHumanoidBotWrapper)]
    *   [(свойство SKSimpleBot.SKSimpleBotWrapper)]

*   [ForwardBackward (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
*   [FromHex() (статический метод Varwin.Color)]

## G

*   [G (атрибут Varwin.Color)]
*   [Get() (статический метод Varwin.DynamicValueDictionary)]
    *   [(статический метод Varwin.Requests)]

*   [GetAll() (статический метод Varwin.Objects)]
*   [GetAncestry() (метод Varwin.Object)]
*   [GetChildren() (метод Varwin.Object)]
*   [GetClones() (статический метод Varwin.Cloning)]
*   [GetContainedObjects() (метод CustomZone.CustomZoneWrapper)]
*   [GetDescendants() (метод Varwin.Object)]
*   [GetDistanceToObject() (метод Varwin.MotionBehaviour)]
*   [GetDistanceToVector() (метод Varwin.MotionBehaviour)]
*   [GetLineBreak() (статический метод Varwin.StringUtils)]
*   [GetName() (метод Varwin.Object)]*   [GetObjectByInstanceId() (статический метод Varwin.Objects)]
*   [GetObjectByVarName() (статический метод Varwin.Objects)]
*   [GetObjectsOfType() (статический метод Varwin.Objects)]
*   [GetParent() (метод Varwin.Object)]
*   [GetRandom() (статический метод Varwin.Color)]
*   [GetRandomLetter() (статический метод Varwin.StringUtils)]
*   [GetRotationAroundAxisToObject() (метод Varwin.RotateBehaviour)]
*   [GetRotationToObject() (метод Varwin.RotateBehaviour)]
*   [GetText() (метод VText.VTextWrapper)]
*   [GetTypeName() (метод Varwin.Object)]
*   [Gravity (свойство Varwin.PhysicsBehaviour)]
*   [GravityOff (атрибут Player.PlayerWrapper.Gravity)]
*   [GravityOn (атрибут Player.PlayerWrapper.Gravity)]
*   [GreenButtonPressed() (метод SKJoystick.SKJoystickWrapper)]

## H

*   [HandsRadius (свойство Player.PlayerWrapper)]
*   [Happy (атрибут VSmile.VSmileWrapper.SmileState)]
*   [Hard (атрибут VDirectionalLight.VDirectionalLightWrapper.LightShadows)]
    *   [(атрибут VPointLight.VPointLightWrapper.LightShadows)]
    *   [(атрибут VSpotLight.VSpotLightWrapper.LightShadows)]

*   [headers (атрибут Varwin.Requests.Response)]*   [HeadPosition (свойство Player.PlayerWrapper)]
*   [HeadRotation (свойство Player.PlayerWrapper)]
*   [HidePlayer() (метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [HorizontalAlignment (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [HorizontalTextAlignment (свойство VText.VTextWrapper)]

## I

*   [Intensity (свойство VDirectionalLight.VDirectionalLightWrapper)]
    *   [(свойство VPointLight.VPointLightWrapper)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]

*   [InteractionBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [InteractionBehaviour.ControllerHand (класс в Varwin)]
*   [InteractionBehaviour.GrabState (класс в Varwin)]
*   [InteractionBehaviour.TeleportState (класс в Varwin)]
*   [InteractionBehaviour.TouchState (класс в Varwin)]
*   [InteractionBehaviour.UseState (класс в Varwin)]
*   [InverseTransformPoint() (метод Varwin.Object)]
*   [IsActive() (метод Varwin.Object)]
*   [IsAffectedByForceNow() (метод Varwin.PhysicsBehaviour)]
*   [IsArcIsHiddenOnDisabledTeleport (свойство Player.PlayerWrapper)]
*   [IsClone() (статический метод Varwin.Cloning)]
*   [IsCloneOfObject() (статический метод Varwin.Cloning)]
*   [IsColorChangingNow() (метод Varwin.VisualizationBehaviour)]
*   [IsContainObject() (метод CustomZone.CustomZoneWrapper)]
*   [IsDestroyed() (статический метод Varwin.Cloning)]
*   [IsDisabled() (метод Varwin.Object)]
*   [IsEnabled() (метод Varwin.Object)]
*   [IsFound() (метод ARMarker.ARMarkerWrapper)]
*   [IsGrabbed() (метод Varwin.InteractionBehaviour)]
*   [IsInactive() (метод Varwin.Object)]
*   [IsLoading() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]*   [IsMouseLookEnabled (свойство Player.PlayerWrapper)]
*   [IsMovingNow() (метод Varwin.MotionBehaviour)]
*   [IsOn() (метод TutorialBulb.TutorialBulbWrapper)]
*   [IsPaused() (метод VarwinAudio.VarwinAudioWrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [IsPlaying() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinAudio.VarwinAudioWrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [IsPressed() (метод TutorialButton.TutorialButtonWrapper)]
*   [IsPrime() (статический метод Varwin.Math)]
*   [IsRotatingNow() (метод Varwin.RotateBehaviour)]
*   [IsScalingNow() (метод Varwin.ScaleBehaviour)]
*   [IsState() (метод VSmile.VSmileWrapper)]
*   [IsStopped() (метод VarwinAudio.VarwinAudioWrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [IsTouching() (метод Varwin.InteractionBehaviour)]
*   [IsTurnInVREnabled (свойство Player.PlayerWrapper)]
*   [IsUsing() (метод Varwin.InteractionBehaviour)]
*   [Italic (свойство VText.VTextWrapper)]
*   [ItalicStyle (свойство TutorialDisplay.TutorialDisplayWrapper)]

## J

*   [Jump() (метод SKHumanoidBot.SKHumanoidBotWrapper)]*   [JumpHeight (свойство Player.PlayerWrapper)]

## K

*   [Keep (атрибут VText.VTextWrapper.KeepProportionOptions)]
*   [KeepTextProportions (свойство VText.VTextWrapper)]*   [Kinematic (атрибут Varwin.PhysicsBehaviour.KinematicState)]
    *   [(свойство Varwin.PhysicsBehaviour)]

## L

*   [LastIndex() (статический метод Varwin.ListUtils)]
*   [Left (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentHorizontalType)]
    *   [(атрибут Varwin.InteractionBehaviour.ControllerHand)]
    *   [(атрибут VBotBoy.VBotBoyWrapper.MovementDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementDirection)]
    *   [(атрибут VText.VTextWrapper.HorizontalAlignment)]

*   [LeftHand (атрибут Player.PlayerWrapper.PlayerHand)]
*   [LeftPadding (свойство VText.VTextWrapper)]
*   [Length (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство VarwinAudio.VarwinAudioWrapper)]
    *   [(свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [Lerp() (статический метод Varwin.Color)]
*   [LinearDrag (свойство Varwin.PhysicsBehaviour)]
*   [ListUtils (класс в Varwin)]
*   [Load() (метод VPanorama.VPanoramaWrapper)]
    *   [(метод VPanorama180.VPanorama180Wrapper)]

*   [LoadAndPlay() (метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [LoadConfigurationByGuid() (статический метод Varwin.Project)]
*   [LoadConfigurationByName() (статический метод Varwin.Project)]
*   [LoadSceneByGuid() (статический метод Varwin.Project)]
*   [LoadSceneByName() (статический метод Varwin.Project)]
*   [LoadVideo() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]*   [LocalX (атрибут Varwin.RotateBehaviour.RotationAxis)]
*   [LocalY (атрибут Varwin.RotateBehaviour.RotationAxis)]
*   [Lock (атрибут StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper.PlayerLockOptions)]
    *   [(атрибут StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper.PlayerLockOptions)]
    *   [(атрибут Varwin.MotionBehaviour.LockRotationRules)]
    *   [(атрибут VarwinVideo180.VarwinVideo180Wrapper.PlayerLockOptions)]
    *   [(атрибут VarwinVideo360.VarwinVideo360Wrapper.PlayerLockOptions)]
    *   [(атрибут VPanorama.VPanoramaWrapper.PlayerLockOptions)]
    *   [(атрибут VPanorama180.VPanorama180Wrapper.PlayerLockOptions)]

*   [Locomotion (атрибут Player.PlayerWrapper.MovementType)]
*   [Log() (статический метод Varwin.Debug)]
*   [LogDeprecatedCodeError() (статический метод Varwin.Debug)]
*   [LogError() (статический метод Varwin.Debug)]
*   [LogWarning() (статический метод Varwin.Debug)]
*   [LookAtObjectWithSpeedAroundAxis() (метод Varwin.RotateBehaviour)]
*   [Loop (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [Looped (атрибут VarwinAudio.VarwinAudioWrapper.LoopState)]
    *   [(атрибут VarwinModel.VarwinModelWrapper.LoopOptions)]
    *   [(атрибут VarwinVideo.VarwinVideoWrapper.LoopBehaviourOptions)]
    *   [(атрибут VarwinVideo180.VarwinVideo180Wrapper.LoopBehaviourOptions)]
    *   [(атрибут VarwinVideo360.VarwinVideo360Wrapper.LoopBehaviourOptions)]

*   [LoopMode (свойство VarwinModel.VarwinModelWrapper)]

## M

*   [Magnitude (свойство Varwin.Vector3)]
*   [Mass (свойство Varwin.PhysicsBehaviour)]
*   [Math (класс в Varwin)]
*   [MaxFontSize (свойство VText.VTextWrapper)]
*   [Method (класс в Varwin)]
*   [Middle (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentVerticalType)]
    *   [(атрибут VText.VTextWrapper.VerticalAlignment)]

*   [MinFontSize (свойство VText.VTextWrapper)]
*   [MinimumTargetStopDistance (свойство Varwin.MotionBehaviour)]
*   [MotionBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [MotionBehaviour.Axis (класс в Varwin)]
*   [MotionBehaviour.LockRotationRules (класс в Varwin)]
*   [MoveAlongPath() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [MoveAlongThePath() (метод Varwin.MotionBehaviour)]
*   [MoveByAxisAtDistance() (метод Varwin.MotionBehaviour)]*   [MoveByAxisOverTime() (метод Varwin.MotionBehaviour)]
*   [MoveByAxisWithSpeed() (метод Varwin.MotionBehaviour)]
*   [MoveByMeters() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [MoveInfinite() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [MovementFaceDirection (свойство Varwin.MotionBehaviour)]
*   [MovementSpeed (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
    *   [(свойство SKSimpleBot.SKSimpleBotWrapper)]

*   [MoveToCoordinatesAtSpeed() (метод Varwin.MotionBehaviour)]
*   [MoveToObject() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [MoveToObjectAtSpeed() (метод Varwin.MotionBehaviour)]
*   [MoveToObjectWithSpeed() (метод Player.PlayerWrapper)]
*   [MoveToPointWithSpeed() (метод Player.PlayerWrapper)]
*   [MuteAudio() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

## N

*   [Neutral (атрибут VSmile.VSmileWrapper.SmileState)]
*   [Never (атрибут VBotBoy.VBotBoyWrapper.TextBubbleHideType)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.TextBubbleHideType)]

*   [None_ (атрибут Varwin.InteractionBehaviour.ControllerHand)]
    *   [(атрибут VDirectionalLight.VDirectionalLightWrapper.LightShadows)]
    *   [(атрибут VPointLight.VPointLightWrapper.LightShadows)]
    *   [(атрибут VSmile.VSmileWrapper.SmileState)]
    *   [(атрибут VSpotLight.VSpotLightWrapper.LightShadows)]*   [NonKinematic (атрибут Varwin.PhysicsBehaviour.KinematicState)]
*   [NonObstacle (атрибут Varwin.PhysicsBehaviour.ObstacleState)]
*   [Normalized (свойство Varwin.Vector3)]
*   [NotLooped (атрибут VarwinModel.VarwinModelWrapper.LoopOptions)]
    *   [(атрибут VarwinVideo.VarwinVideoWrapper.LoopBehaviourOptions)]
    *   [(атрибут VarwinVideo180.VarwinVideo180Wrapper.LoopBehaviourOptions)]
    *   [(атрибут VarwinVideo360.VarwinVideo360Wrapper.LoopBehaviourOptions)]

*   [NotSave (атрибут TutorialDisplay.TutorialDisplayWrapper.ProportionType)]

## O

*   [Object (класс в Varwin)]
*   [ObjectInteraction (свойство Player.PlayerWrapper)]
*   [Objects (класс в Varwin)]
*   [Obstacle (атрибут Varwin.PhysicsBehaviour.ObstacleState)]
    *   [(свойство Varwin.PhysicsBehaviour)]*   [Off (атрибут Varwin.PhysicsBehaviour.GravityState)]
    *   [(атрибут Varwin.VisualizationBehaviour.ShadowCastingMode)]

*   [On (атрибут Varwin.PhysicsBehaviour.GravityState)]
    *   [(атрибут Varwin.VisualizationBehaviour.ShadowCastingMode)]

*   [OnlyHorizontal (атрибут Varwin.MotionBehaviour.LockRotationRules)]
*   [OpenUrl() (статический метод Varwin.Application)]

## P

*   [PaddingBottom (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [PaddingLeft (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [PaddingRight (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [PaddingTop (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [PanelColor (свойство VText.VTextWrapper)]
*   [Pause (атрибут Varwin.VisualizationBehaviour.PlayableState)]
*   [Pause() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод Varwin.MotionBehaviour)]
    *   [(метод Varwin.PhysicsBehaviour)]
    *   [(метод Varwin.RotateBehaviour)]
    *   [(метод Varwin.ScaleBehaviour)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [PauseAnimation() (метод VarwinModel.VarwinModelWrapper)]
*   [PausePath() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [PauseSound() (метод VarwinAudio.VarwinAudioWrapper)]
*   [PhysicsBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [PhysicsBehaviour.GravityState (класс в Varwin)]
*   [PhysicsBehaviour.KinematicState (класс в Varwin)]
*   [PhysicsBehaviour.ObstacleState (класс в Varwin)]
*   [PhysicsBehaviour.Relativeness (класс в Varwin)]
*   [PingPong (атрибут VarwinModel.VarwinModelWrapper.AnimationPlayTypeOptions)]
*   [Play() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [PlayAnimation() (метод VarwinModel.VarwinModelWrapper)]
*   [PlaybackLoopState (свойство VarwinAudio.VarwinAudioWrapper)]*   [PlayerLockMode (свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]
    *   [(свойство VPanorama.VPanoramaWrapper)]
    *   [(свойство VPanorama180.VPanorama180Wrapper)]

*   [PlayerNormalHeight (свойство Player.PlayerWrapper)]
*   [PlayerWrapper (класс в Player)]
*   [PlayerWrapper.AllowedStates (класс в Player)]
*   [PlayerWrapper.Gravity (класс в Player)]
*   [PlayerWrapper.MovementType (класс в Player)]
*   [PlayerWrapper.PlayerHand (класс в Player)]
*   [PlayerWrapper.RotationTypes (класс в Player)]
*   [PlayerWrapper.SwitchStateTypes (класс в Player)]
*   [PlayerWrapper.VibrationPreset (класс в Player)]
*   [PlayOnAwake (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [PlaySound() (метод VarwinAudio.VarwinAudioWrapper)]
*   [PointerLength (свойство Player.PlayerWrapper)]
*   [Position (свойство Varwin.MotionBehaviour)]
*   [PositionX (свойство Varwin.MotionBehaviour)]
*   [PositionY (свойство Varwin.MotionBehaviour)]
*   [PositionZ (свойство Varwin.MotionBehaviour)]
*   [Post() (статический метод Varwin.Requests)]
*   [Prohibited (атрибут Player.PlayerWrapper.AllowedStates)]
*   [ProhibitMovementType() (метод Player.PlayerWrapper)]
*   [Project (класс в Varwin)]
*   [Property (класс в Varwin)]
*   [Proportion (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [PtSerif (атрибут TutorialDisplay.TutorialDisplayWrapper.Fonts)]
    *   [(атрибут VText.VTextWrapper.Fonts)]

*   [Put() (статический метод Varwin.Requests)]

## R

*   [R (атрибут Varwin.Color)]
*   [RandFloat() (статический метод Varwin.Random)]
*   [RandInt() (статический метод Varwin.Random)]
*   [Random (класс в Varwin)]
*   [Range (класс в Varwin)]
    *   [(свойство VPointLight.VPointLightWrapper)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]

*   [RedButtonPressed() (метод SKJoystick.SKJoystickWrapper)]
*   [Replace() (статический метод Varwin.StringUtils)]
*   [Requests (класс в Varwin)]
*   [Requests.Request (класс в Varwin)]
*   [Requests.Response (класс в Varwin)]
*   [ResetSpeed() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [RestartScene() (статический метод Varwin.Project)]
*   [Reverse (атрибут VarwinModel.VarwinModelWrapper.AnimationPlayTypeOptions)]
*   [Right (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentHorizontalType)]
    *   [(атрибут Varwin.InteractionBehaviour.ControllerHand)]
    *   [(атрибут VBotBoy.VBotBoyWrapper.MovementDirection)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementDirection)]
    *   [(атрибут VText.VTextWrapper.HorizontalAlignment)]

*   [RightHand (атрибут Player.PlayerWrapper.PlayerHand)]
*   [RightLeft (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
*   [RightPadding (свойство VText.VTextWrapper)]
*   [RobotoMono (атрибут TutorialDisplay.TutorialDisplayWrapper.Fonts)]
    *   [(атрибут VText.VTextWrapper.Fonts)]*   [Rotate() (статический метод Varwin.Vector3)]
*   [RotateAroundAnotherObjectAxisWithSpeed() (метод Varwin.RotateBehaviour)]
*   [RotateAroundAxis() (метод Varwin.RotateBehaviour)]
*   [RotateAroundAxisByAngleWithSpeed() (метод Varwin.RotateBehaviour)]
*   [RotateAroundAxisWithSpeed() (метод Varwin.RotateBehaviour)]
*   [RotateAsObject() (метод Varwin.RotateBehaviour)]
*   [RotateAsObjectWithSpeed() (метод Varwin.RotateBehaviour)]
*   [RotateBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [RotateBehaviour.Axis (класс в Varwin)]
*   [RotateBehaviour.RotationAxis (класс в Varwin)]
*   [RotateByAngle() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [RotateHorizontally() (метод Player.PlayerWrapper)]
*   [RotateTo() (метод Player.PlayerWrapper)]
*   [RotateToObjectAroundAxis() (метод Varwin.RotateBehaviour)]
*   [RotateToVectorWithSpeed() (метод Varwin.RotateBehaviour)]
*   [Rotation (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
    *   [(свойство SKHumanoidBot.SKHumanoidBotWrapper)]
    *   [(свойство SKSimpleBot.SKSimpleBotWrapper)]

*   [RotationAroundAxisWithSpeedOverTime() (метод Varwin.RotateBehaviour)]
*   [RotationSpeed (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
    *   [(свойство SKSimpleBot.SKSimpleBotWrapper)]

*   [Run (атрибут VBotBoy.VBotBoyWrapper.MovementPace)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementPace)]

*   [Run() (статический метод Varwin.Async)]

## S

*   [Sad (атрибут VSmile.VSmileWrapper.SmileState)]
*   [SameAsObject (атрибут Player.PlayerWrapper.RotationTypes)]
*   [Save (атрибут TutorialDisplay.TutorialDisplayWrapper.ProportionType)]
    *   [(атрибут VText.VTextWrapper.KeepProportionOptions)]

*   [SayText() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SayTextWith() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [Scale (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство Varwin.ScaleBehaviour)]
    *   [(свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [ScaleBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [ScaleByFactorOverTime() (метод Varwin.ScaleBehaviour)]
*   [ScaleOverTime() (метод Varwin.ScaleBehaviour)]
*   [ScaleX (свойство Varwin.ScaleBehaviour)]
*   [ScaleY (свойство Varwin.ScaleBehaviour)]
*   [ScaleZ (свойство Varwin.ScaleBehaviour)]
*   [Seek() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinAudio.VarwinAudioWrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [Self (атрибут Varwin.PhysicsBehaviour.Relativeness)]
*   [SetAnimationByIndex() (метод VarwinModel.VarwinModelWrapper)]
*   [SetChangingColorState() (метод Varwin.VisualizationBehaviour)]
*   [SetEulerAngles() (метод Player.PlayerWrapper)]
*   [SetLoopBehaviour (свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [SetMaxStepHeight() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SetMaxTraversableSlope() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SetMinObjectDistance() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SetPosition() (метод Varwin.MotionBehaviour)]
*   [SetPressedState() (метод TutorialButton.TutorialButtonWrapper)]
*   [SetReleasedState() (метод TutorialButton.TutorialButtonWrapper)]
*   [SetRotation() (метод Varwin.RotateBehaviour)]
*   [SetScale() (метод Varwin.ScaleBehaviour)]
*   [SetShowTextBubble() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SetShowTextBubbleHideType() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [SetState() (метод VSmile.VSmileWrapper)]
*   [SetText() (метод TutorialDisplay.TutorialDisplayWrapper)]
    *   [(метод VText.VTextWrapper)]

*   [Shadows (свойство VDirectionalLight.VDirectionalLightWrapper)]
    *   [(свойство VPointLight.VPointLightWrapper)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]*   [ShadowsOnly (атрибут Varwin.VisualizationBehaviour.ShadowCastingMode)]
*   [ShadowStrength (свойство VDirectionalLight.VDirectionalLightWrapper)]
    *   [(свойство VPointLight.VPointLightWrapper)]
    *   [(свойство VSpotLight.VSpotLightWrapper)]

*   [ShortCircuit() (метод SKSimpleBot.SKSimpleBotWrapper)]
*   [ShowPlayer() (метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [Size (свойство VText.VTextWrapper)]
*   [SKCoinWrapper (класс в SKCoin)]
*   [SKFlyingDroneWrapper (класс в SKFlyingDrone)]
*   [SKHumanoidBotWrapper (класс в SKHumanoidBot)]
*   [SKJoystickWrapper (класс в SKJoystick)]
*   [SKLadderWrapper (класс в SKLadder)]
*   [SKSimpleBotWrapper (класс в SKSimpleBot)]
*   [Soft (атрибут VDirectionalLight.VDirectionalLightWrapper.LightShadows)]
    *   [(атрибут VPointLight.VPointLightWrapper.LightShadows)]
    *   [(атрибут VSpotLight.VSpotLightWrapper.LightShadows)]

*   [SortingOrder (свойство VarwinImage.VarwinImageWrapper)]
    *   [(свойство VText.VTextWrapper)]

*   [Speed (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство Varwin.PhysicsBehaviour)]
    *   [(свойство VarwinAudio.VarwinAudioWrapper)]
    *   [(свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [SphereColliderWrapper (класс в SphereCollider)]
*   [SprintSpeed (свойство Player.PlayerWrapper)]
*   [StartApplyingForceInDirectionRelativeTo() (метод Varwin.PhysicsBehaviour)]
*   [status_code (атрибут Varwin.Requests.Response)]
*   [Stop (атрибут Varwin.VisualizationBehaviour.PlayableState)]
*   [Stop() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод Varwin.MotionBehaviour)]
    *   [(метод Varwin.PhysicsBehaviour)]
    *   [(метод Varwin.RotateBehaviour)]
    *   [(метод Varwin.ScaleBehaviour)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]

*   [StopAnimation() (метод VarwinModel.VarwinModelWrapper)]
*   [StopMovement() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [StopSound() (метод VarwinAudio.VarwinAudioWrapper)]
*   [StopSpeaking() (метод VBotBoy.VBotBoyWrapper)]
    *   [(метод VBotGirl.VBotGirlWrapper)]

*   [StreamingVarwinVideo180Wrapper (класс в StreamingVarwinVideo180)]
*   [StreamingVarwinVideo180Wrapper.PlayerLockOptions (класс в StreamingVarwinVideo180)]
*   [StreamingVarwinVideo360Wrapper (класс в StreamingVarwinVideo360)]
*   [StreamingVarwinVideo360Wrapper.PlayerLockOptions (класс в StreamingVarwinVideo360)]
*   [StreamingVarwinVideoWrapper (класс в StreamingVarwinVideo)]
*   [Strikethrough (свойство VText.VTextWrapper)]
*   [StrikethroughStyle (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [StringUtils (класс в Varwin)]
*   [Strong (атрибут Player.PlayerWrapper.VibrationPreset)]

## T

*   [T (атрибут Varwin.Cloning)]
    *   [(атрибут Varwin.Objects)]

*   [Teleport (атрибут Player.PlayerWrapper.MovementType)]
*   [TeleportPlayerInPanorama() (метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]
    *   [(метод VPanorama.VPanoramaWrapper)]
    *   [(метод VPanorama180.VPanorama180Wrapper)]

*   [TeleportTo() (метод Varwin.MotionBehaviour)]
*   [TeleportToObject() (метод Player.PlayerWrapper)]
*   [TeleportToStartPosition() (метод Player.PlayerWrapper)]
*   [TeleportToVector() (метод Player.PlayerWrapper)]
*   [text (атрибут Varwin.Requests.Response)]
*   [TextColor (свойство TutorialDisplay.TutorialDisplayWrapper)]
    *   [(свойство VText.VTextWrapper)]*   [TextFont (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [ToObject (атрибут Player.PlayerWrapper.RotationTypes)]
*   [Top (атрибут TutorialDisplay.TutorialDisplayWrapper.AlignmentVerticalType)]
    *   [(атрибут VText.VTextWrapper.VerticalAlignment)]

*   [TopPadding (свойство VText.VTextWrapper)]
*   [TransformPoint() (метод Varwin.Object)]
*   [TrueWithProbability() (статический метод Varwin.Random)]
*   [TurnOff() (метод TutorialBulb.TutorialBulbWrapper)]
*   [TurnOn() (метод TutorialBulb.TutorialBulbWrapper)]
*   [TutorialBulbWrapper (класс в TutorialBulb)]
*   [TutorialButtonWrapper (класс в TutorialButton)]
*   [TutorialDisplayWrapper (класс в TutorialDisplay)]
*   [TutorialDisplayWrapper.AlignmentHorizontalType (класс в TutorialDisplay)]
*   [TutorialDisplayWrapper.AlignmentVerticalType (класс в TutorialDisplay)]
*   [TutorialDisplayWrapper.Fonts (класс в TutorialDisplay)]
*   [TutorialDisplayWrapper.ProportionType (класс в TutorialDisplay)]
*   [TwoSided (атрибут Varwin.VisualizationBehaviour.ShadowCastingMode)]

## U

*   [Ubuntu (атрибут TutorialDisplay.TutorialDisplayWrapper.Fonts)]
    *   [(атрибут VText.VTextWrapper.Fonts)]

*   [Underline (свойство VText.VTextWrapper)]
*   [UnderlinedStyle (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [Unload() (метод VPanorama.VPanoramaWrapper)]
    *   [(метод VPanorama180.VPanorama180Wrapper)]

*   [UnloadVideo() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(метод VarwinVideo.VarwinVideoWrapper)]
    *   [(метод VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(метод VarwinVideo360.VarwinVideo360Wrapper)]*   [Unlooped (атрибут VarwinAudio.VarwinAudioWrapper.LoopState)]
*   [UnmuteAudio() (метод StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(метод StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(метод StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]

*   [UpDown (свойство SKFlyingDrone.SKFlyingDroneWrapper)]
*   [UseGravity (свойство Player.PlayerWrapper)]
*   [UserType (класс в Varwin)]

## V

*   [Value (свойство Varwin.Variable)]
*   [Variable (класс в Varwin)]
*   [VarwinAudioWrapper (класс в VarwinAudio)]
*   [VarwinAudioWrapper.LoopState (класс в VarwinAudio)]
*   [VarwinImageWrapper (класс в VarwinImage)]
*   [VarwinModelWrapper (класс в VarwinModel)]
*   [VarwinModelWrapper.AnimationPlayTypeOptions (класс в VarwinModel)]
*   [VarwinModelWrapper.LoopOptions (класс в VarwinModel)]
*   [VarwinVideo180Wrapper (класс в VarwinVideo180)]
*   [VarwinVideo180Wrapper.LoopBehaviourOptions (класс в VarwinVideo180)]
*   [VarwinVideo180Wrapper.PlayerLockOptions (класс в VarwinVideo180)]
*   [VarwinVideo360Wrapper (класс в VarwinVideo360)]
*   [VarwinVideo360Wrapper.LoopBehaviourOptions (класс в VarwinVideo360)]
*   [VarwinVideo360Wrapper.PlayerLockOptions (класс в VarwinVideo360)]
*   [VarwinVideoWrapper (класс в VarwinVideo)]
*   [VarwinVideoWrapper.LoopBehaviourOptions (класс в VarwinVideo)]
*   [VBotBoyWrapper (класс в VBotBoy)]
*   [VBotBoyWrapper.MovementDirection (класс в VBotBoy)]
*   [VBotBoyWrapper.MovementPace (класс в VBotBoy)]
*   [VBotBoyWrapper.RotationDirection (класс в VBotBoy)]
*   [VBotBoyWrapper.TextBubbleHideType (класс в VBotBoy)]
*   [VBotGirlWrapper (класс в VBotGirl)]
*   [VBotGirlWrapper.MovementDirection (класс в VBotGirl)]
*   [VBotGirlWrapper.MovementPace (класс в VBotGirl)]
*   [VBotGirlWrapper.RotationDirection (класс в VBotGirl)]
*   [VBotGirlWrapper.TextBubbleHideType (класс в VBotGirl)]
*   [VConeWrapper (класс в VCone)]
*   [VCubeWrapper (класс в VCube)]
*   [VCylinderWrapper (класс в VCylinder)]
*   [VDirectionalLightWrapper (класс в VDirectionalLight)]
*   [VDirectionalLightWrapper.LightShadows (класс в VDirectionalLight)]
*   [Vector3 (класс в Varwin)]
*   [VEmptyObjectWrapper (класс в VEmptyObject)]
*   [VerticalAlignment (свойство TutorialDisplay.TutorialDisplayWrapper)]
*   [VerticalTextAlignment (свойство VText.VTextWrapper)]*   [VHexagonWrapper (класс в VHexagon)]
*   [VibrateLeftHand() (метод Player.PlayerWrapper)]
*   [VibrateLeftHandPreset() (метод Player.PlayerWrapper)]
*   [VibrateRightHand() (метод Player.PlayerWrapper)]
*   [VibrateRightHandPreset() (метод Player.PlayerWrapper)]
*   [VibrateWithIntervals() (метод Player.PlayerWrapper)]
*   [VisualizationBehaviour (класс в Varwin)]
    *   [(свойство Varwin.Object)]

*   [VisualizationBehaviour.PlayableState (класс в Varwin)]
*   [VisualizationBehaviour.ShadowCastingMode (класс в Varwin)]
*   [Volume (свойство StreamingVarwinVideo.StreamingVarwinVideoWrapper)]
    *   [(свойство StreamingVarwinVideo180.StreamingVarwinVideo180Wrapper)]
    *   [(свойство StreamingVarwinVideo360.StreamingVarwinVideo360Wrapper)]
    *   [(свойство VarwinAudio.VarwinAudioWrapper)]
    *   [(свойство VarwinVideo.VarwinVideoWrapper)]
    *   [(свойство VarwinVideo180.VarwinVideo180Wrapper)]
    *   [(свойство VarwinVideo360.VarwinVideo360Wrapper)]

*   [VPanorama180Wrapper (класс в VPanorama180)]
*   [VPanorama180Wrapper.PlayerLockOptions (класс в VPanorama180)]
*   [VPanoramaWrapper (класс в VPanorama)]
*   [VPanoramaWrapper.PlayerLockOptions (класс в VPanorama)]
*   [VPlaneWrapper (класс в VPlane)]
*   [VPointLightWrapper (класс в VPointLight)]
*   [VPointLightWrapper.LightShadows (класс в VPointLight)]
*   [VPyramidWrapper (класс в VPyramid)]
*   [VSmileWrapper (класс в VSmile)]
*   [VSmileWrapper.SmileState (класс в VSmile)]
*   [VSphereWrapper (класс в VSphere)]
*   [VSpotLightWrapper (класс в VSpotLight)]
*   [VSpotLightWrapper.LightShadows (класс в VSpotLight)]
*   [VTextWrapper (класс в VText)]
*   [VTextWrapper.Fonts (класс в VText)]
*   [VTextWrapper.HorizontalAlignment (класс в VText)]
*   [VTextWrapper.KeepProportionOptions (класс в VText)]
*   [VTextWrapper.VerticalAlignment (класс в VText)]

## W

*   [WaitForEndOfFrame (класс в Varwin)]
*   [WaitForSeconds (класс в Varwin)]
*   [WaitWhile (класс в Varwin)]
*   [Walk (атрибут VBotBoy.VBotBoyWrapper.MovementPace)]
    *   [(атрибут VBotGirl.VBotGirlWrapper.MovementPace)]*   [WalkingSpeed (свойство Player.PlayerWrapper)]
*   [Weak (атрибут Player.PlayerWrapper.VibrationPreset)]
*   [WoodenoldtableWrapper (класс в Woodenoldtable)]
*   [World (атрибут Varwin.PhysicsBehaviour.Relativeness)]

## X

*   [X (атрибут Varwin.MotionBehaviour.Axis)]
    *   [(атрибут Varwin.RotateBehaviour.Axis)]
    *   [(атрибут Varwin.Vector3)]

## Y

*   [Y (атрибут Varwin.MotionBehaviour.Axis)]
    *   [(атрибут Varwin.RotateBehaviour.Axis)]
    *   [(атрибут Varwin.Vector3)]*   [YellowButtonPressed() (метод SKJoystick.SKJoystickWrapper)]

## Z

*   [Z (атрибут Varwin.MotionBehaviour.Axis)]
    *   [(атрибут Varwin.RotateBehaviour.Axis)]
    *   [(атрибут Varwin.Vector3)]

########## index.html.md
Title: Varwin Python API Documentation — документация Varwin 18

Добро пожаловать в официальную документацию Python API для Varwin — платформы для создания и управления виртуальными мирами и интерактивными симуляциями.

Эта документация предназначена для разработчиков, интеграторов и преподавателей, использующих Python для расширения возможностей Varwin: от автоматизации сценариев и управления объектами до создания сложных образовательных и игровых сред.

Что вы найдёте здесь

*   [Структура проекта]

*   [Асинхронное программирование]

*   [Отправка запросов]

*   [Примеры использования — готовые фрагменты кода]

*   [API стандартной функциональности]

*   [Основная документация]

########## pages_api.html.md

*   [Varwin]
*   [Базовые объекты]

########## pages_async.html.md
Title: Асинхронное программирование — документация Varwin 18

## Асинхронное программирование[]

Для реализации сценариев с асинхронным поведением — таких как последовательные анимации, задержки, ожидание условий или неблокирующее выполнение логики — платформа Varwin предоставляет встроенную поддержку корутин на основе синтаксиса `async`/`await`.

В отличие от стандартной библиотеки `asyncio`, асинхронная модель Varwin интегрирована напрямую с игровым циклом движка и гарантирует, что весь пользовательский код выполняется **в основном потоке**, где доступны все объекты сцены и их методы.

## Класс `Varwin.Async`[]

Основной точкой входа для работы с корутинами является класс `Varwin.Async`. Он предоставляет методы для регистрации и запуска асинхронных функций в контексте жизненного цикла сцены.

Основные методы:

*   `Varwin.Async.Run(coro)` — немедленно запускает переданную корутину.

*   `Varwin.Async.AddStart(coro_func)` — регистрирует асинхронную функцию (не результат вызова!), которая будет запущена один раз при старте сцены.

*   `Varwin.Async.AddUpdate(coro_func)` — регистрирует асинхронную функцию, вызываемую зацикленно (аналогично `Update` в Unity, но с поддержкой `await`).

Пример использования:

async def Chain2():
    # Масштабируем объект в течение 1 секунды
    await cube10.ScaleBehaviour.ScaleOverTime(Varwin.Vector3(7, 1, 1), 1)
    # Ждём 2 секунды
    await Varwin.WaitForSeconds(2)
    # Возвращаем исходный масштаб
    await cube10.ScaleBehaviour.ScaleOverTime(Varwin.Vector3(1, 1, 1), 1)

# Запуск корутины
Varwin.Async.Run(Chain2())

Обратите внимание: при использовании `AddStart` и `AddUpdate` передаётся **сама функция**, а не её вызов:

Varwin.Async.AddStart(Chain2)  # ✅ правильно
# Varwin.Async.AddStart(Chain2()) # ❌ ошибка: функция уже вызвана

## Встроенные await-объекты[]

Для организации задержек и синхронизации с игровым циклом Varwin предоставляет специальные awaitable-объекты. Они приостанавливают выполнение корутины до наступления определённого события.

Доступные типы:

*   [WaitForSeconds] — приостанавливает выполнение на заданное количество секунд.

*   [WaitForEndOfFrame] — приостанавливает выполнение до конца текущего кадра.

*   [WaitWhile] — приостанавливает выполнение, пока заданное условие (callable) возвращает `True`.

Пример с `WaitWhile`:

async def WaitCubeMoving():
    await Varwin.WaitWhile(lambda: cube.MotionBehaviour.Position.X < 5.0)
    Varwin.Debug.Log("Куб достиг позиции X=5!")

**Не используйте стандартную библиотеку asyncio** для взаимодействия с объектами сцены. Все компоненты движка (включая трансформации, поведения, события) доступны **только в основном потоке**, в то время как `asyncio` может выполнять код в фоновых потоках или событийных циклах, не связанных с игровым циклом. Это приведёт к ошибкам или неопределённому поведению.

## Рекомендации[]

*   Используйте корутины для последовательных сценариев: анимации → задержка → звук → включение триггера.

*   Избегайте блокирующих вызовов (например, `time.sleep()`) — они остановят весь движок.

*   Всегда предпочитайте `await Varwin.WaitForSeconds(...)` вместо синхронных задержек.

*   Для параллельного выполнения нескольких задач запускайте несколько корутин через `Varwin.Async.Run()`.

Корутины в Varwin — это безопасный и удобный способ писать читаемую, последовательную логику без явного управления состояниями или таймерами.

########## pages_examples.html.md
Title: Примеры использования — документация Varwin 18

## Примеры использования[]

Ниже приведены типовые сценарии применения Python API Varwin в реальных проектах. Примеры охватывают управление объектами, асинхронные сценарии, взаимодействие с пользователем и интеграцию с внешними системами.

## Автоматизация учебного сценария[]

Создание последовательного обучающего процесса с визуальной обратной связью:

async def TrainingSequence():
    # Появление инструкции
    instruction.Activate()
    await Varwin.WaitForSeconds(3)
    instruction.Deactivate()

    # Активация оборудования
    machine.Activate()
    await Varwin.WaitForSeconds(1)

    # Ожидание правильного действия от пользователя
    await Varwin.WaitWhile(lambda: not valve.IsOpen)
    success_sound.Play()
    await Varwin.WaitForSeconds(2)

    # Завершение этапа
    stage_complete.Activate()

Varwin.Async.AddStart(TrainingSequence)

## Взаимодействие с Yandex GPT[]

Использование облачной языковой модели Yandex GPT для генерации контекстно-зависимых ответов или подсказок в симуляции:

import json

async def GetHintFromGPT(context: str):
    # Токен и каталог из настроек Yandex Cloud
    iam_token = "YOUR_IAM_TOKEN"
    folder_id = "YOUR_FOLDER_ID"

    payload = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "50"
        },
        "messages": [
            {"role": "system", "text": "Ты — помощник в VR-тренажёре по технике безопасности."},
            {"role": "user", "text": f"Пользователь не может открыть аварийный клапан. Контекст: {context}"}
    }

    response = await Varwin.Requests.Post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        json=payload,
        headers={
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 200:
        data = json.loads(response.text)
        hint_text = data["result"]["alternatives"][0]["message"]["text"]
        hint_ui.SetText(hint_text)
        hint_ui.Show()
    else:
        Varwin.Debug.LogError(f"Ошибка GPT: {response.status_code}")

# Вызывается при нажатии кнопки "Подсказка"
Varwin.Async.Run(GetHintFromGPT("Клапан заклинило, требуется повернуть рычаг против часовой стрелки."))

## Реакция на события сцены[]

Обработка взаимодействия пользователя с объектами в реальном времени:

def OnAlarmButtonPressed(sender):
    alarm.Play()
    door.Lock()
    Varwin.Async.Run(StartEmergencyProtocol())

# Регистрация обработчика
alarmButton.AddButtonPressedHandler(OnAlarmButtonPressed)

Эти примеры демонстрируют, как Python API Varwin позволяет создавать гибкие, интерактивные и интегрируемые VR-сценарии — от простых обучающих заданий до сложных промышленных симуляций.

########## pages_maindoc.html.md
Title: .Добро пожаловать в базу знаний Varwin v18

![Image 1](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/warning-macro-icon.svg)

Сейчас вы находитесь в документации для **Varwin 18.***

Убедитесь, что вы используете документацию, соответствующую вашей версии платформы

[![Image 2](https://docs.varwin.com/files/latest/ru/2358444802/2358447369/1/1766411306586/image-2025-12-22_16-48-24.png)](https://docs.varwin.com/files/latest/ru/2358444802/2358447369/1/1766411306586/image-2025-12-22_16-48-24.png)

## **Varwin 18.0**

Добро пожаловать в новую эру обучения программированию на платформе Varwin!  
С версией 18.0 мы представляем полноценную образовательную траекторию — от визуального программирования на Blockly до изучения Python, одного из самых популярных языков в образовании и промышленности.

## **🐍 Varwin Python: переход от блоков к коду**[![Image 3: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

[![Image 4](https://docs.varwin.com/files/latest/ru/2358444802/2358444811/1/1766388680398/image-2025-12-22_10-31-19.png)](https://docs.varwin.com/files/latest/ru/2358444802/2358444811/1/1766388680398/image-2025-12-22_10-31-19.png)

**Varwin Python**— это расширение лицензии Varwin Education, которое позволяет писать код на Python в дополнение к Blockly.  
Вы можете:

*   Создавать логику проекта на Blockly, на Python или одновременно на обоих.

*   Работать в единой среде, плавно переходя от визуального программирования к текстовому.

*   Использовать чистый Python с поддержкой всех его возможностей.

> Python — один из языков, на котором решаются задачи ЕГЭ и ОГЭ по информатике.  
> Изучение Python на Varwin даёт ученикам практические навыки для успешной сдачи экзаменов.

## **Новый подход к изучению Python**[![Image 5: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

[![Image 6](https://docs.varwin.com/files/latest/ru/2358444802/2358444810/1/1766388585652/image-2025-12-22_10-29-45.png)](https://docs.varwin.com/files/latest/ru/2358444802/2358444810/1/1766388585652/image-2025-12-22_10-29-45.png)

Ключевое преимущество Varwin —**контекстно-ориентированное обучение**, где каждая строка кода сразу воплощается в интерактивный результат:

*   Вместо абстрактных задач в консоли — оживление объектов, изменение физики мира, диалоги с персонажами.

*   Геймификация обучения: циклы, условия, функции изучаются через создание механик 3D/VR-игр и виртуальных миров.

*   Программирование становится ключом к творчеству и глубокому пониманию языка.

## **Преимущества Python на Varwin**[![Image 7: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

*   Расширение аудитории— поддержка разных возрастов и уровней подготовки.

*   Плавный переход от визуального к текстовому программированию.

*   Соответствие стандартам:

    *   ФГОС по информатике

    *   Заданиям ЕГЭ и ОГЭ

    *   Требованиям IT-рынка

*   Снятие технических ограничений:

    *   Доступ ко всем библиотекам Python

    *   Подключение внешних API и модулей

    *   Неограниченная функциональность

*   Создание сложных проектов— от учебных задач до коммерческих решений.

## **Искусственный интеллект на Varwin Python**[![Image 8: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

Python — язык ИИ, и на Varwin вы можете:

*   Использовать богатую экосистему библиотек:**TensorFlow, PyTorch**и другие.

*   Интегрировать внешние ИИ-сервисы, например**YandexGPT**.

*   Встраивать готовые AI-модели без глубоких знаний в машинном обучении.

*   Создавать уникальные AI-продукты прямо в платформе.

**Пример использования ИИ на Varwin Python:**

[Смотреть видео-кейс](https://vk.com/video-202105375_456239566)

## **Единая образовательная траектория**[![Image 9: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

**[![Image 10](https://docs.varwin.com/files/latest/ru/2358444802/2358444813/1/1766388868572/image-2025-12-22_10-34-27.png)](https://docs.varwin.com/files/latest/ru/2358444802/2358444813/1/1766388868572/image-2025-12-22_10-34-27.png)**

Теперь Varwin объединяет визуальное и текстовое программирование в одну логичную систему.  
Начните с Blockly, постепенно переходите к Python — обучение становится проще, интереснее и эффективнее для любого возраста.

### Начните сегодня![![Image 11: Link to Начните сегодня!](https://docs.varwin.com/_/7F000101018E327DDCEC3A891E2AEEE1/1737625346148/images/common/link-solid.svg)]

Varwin Python уже доступен в версии 18.0.  
Присоединяйтесь к сообществу педагогов и разработчиков, которые создают будущее образования с помощью интерактивного, контекстного и творческого подхода к программированию.

########## pages_project.html.md
Title: Структура проекта — документация Varwin 18

## Структура проекта[]

## Структура файлов и папок[]

При создании проекта в среде Varwin автоматически формируется следующая иерархия файлов и директорий:

├── Blockly.py
├── Main.py
└── Varwin/
 ├── Varwin.py
 ├── SceneObjectTypes.py
 ├── SceneObjects.py
 └── Objects/

Каждый элемент этой структуры играет определённую роль в архитектуре приложения.

## Blockly.py[]

**Тип файла**: только для чтения

**Назначение**: содержит логику, сгенерированную визуальным редактором блоков (Blockly).

Этот модуль автоматически обновляется при изменении в визуальном редакторе.

## Main.py[]

**Тип файла**: редактируемый

**Назначение**: основная точка входа в приложение.

Этот файл предназначен для подключения пользовательских модулей, расширения или переопределения поведения, заданного в `Blockly.py`, а также для реализации кастомной логики.

Пример содержимого:

import Varwin
from SceneObjects import *
import Blockly

async def OnStart():
    # Пользовательская инициализация при запуске сцены
    pass

async def OnUpdate():
    # Логика, выполняемая зацикленно
    pass

# Регистрация пользовательских обработчиков
Varwin.Async.AddStart(OnStart)
Varwin.Async.AddUpdate(OnUpdate)

**Тип файла**: только для чтения

**Назначение**: предоставляет API для взаимодействия с объектами сцены, системными событиями и служебными функциями.

Основные возможности:

*   Управление жизненным циклом сцены (например, `Varwin.Async.AddStart`)

*   Отладочный вывод (`Varwin.Debug.Log`)

*   Доступ к объектам сцены

*   Реализация корутин

*   Стандартные поведения

Полный перечень доступных классов, функций и методов с сигнатурами, параметрами и примерами использования приведён в разделе:

[Varwin]

## SceneObjectTypes.py[]

**Тип файла**: только для чтения

**Назначение**: маппинг технических имён типов объектов на удобочитаемые псевдонимы.

Внутренние имена объектов имеют формат `<C#_TypeName>_<Root_GUID>`. Этот модуль заменяет их на короткие и понятные имена.

Если в проекте обнаружены конфликтующие имена (два разных типа с одинаковым псевдонимом), система автоматически использует полное имя с GUID, чтобы избежать неоднозначности.

## SceneObjects.py[]

**Тип файла**: только для чтения

**Назначение**: содержит экземпляры всех объектов, размещённых на сцене.

Каждый объект представлен как переменная с именем, заданным в поле **«Имя переменной»** в редакторе сцены.

Пример:

from SceneObjectTypes import *

# В редакторе сцены задано имя переменной: player
player = PlayerWrapper(...)

Этот модуль автоматически генерируется и обновляется при изменении сцены.

Совет

Используйте `from SceneObjects import *` в `Main.py` или других модулях для прямого доступа к объектам по их именам.

## Пользовательские модули[]

**Тип файла**: редактируемый

**Назначение**: расширение функциональности приложения.

Varwin поддерживает **модульную архитектуру**, позволяя разделять логику на независимые Python-файлы.

Преимущества:

*   **Читаемость**: каждая функциональная область вынесена в отдельный файл.

*   **Изоляция**: каждый модуль имеет собственное пространство имён.

*   **Повторное использование**: модули легко импортировать в других проектах.

*   **Автоматическая загрузка**: платформа управляет порядком инициализации (при отсутствии циклических зависимостей).

Как использовать:

1.   Создайте новый Python-файл (например, `movement.py`).

2.   Реализуйте в нём нужную логику.

3.   Импортируйте модуль в `Main.py` или другом месте.

Пример:

Файл `MyModule.py`:

import Varwin

def hello():
    Varwin.Debug.Log("Привет, Мир!")

Файл `Main.py`:

import Varwin
import MyModule

async def OnStart():
    MyModule.hello()

Varwin.Async.AddStart(OnStart)

Совет

Группируйте связанную логику в отдельные модули:

*   `movement.py` — управление перемещением объектов

*   `sensors.py` — обработка данных с датчиков

*   `ui.py` — взаимодействие с пользовательским интерфейсом

*   `ai.py` — поведенческие алгоритмы

########## pages_requests.html.md
Title: Отправка запросов — документация Varwin 18

## Отправка запросов[]

Для выполнения HTTP-запросов в пользовательском коде рекомендуется использовать встроенный класс `Varwin.Requests`.

В отличие от сторонних HTTP-клиентов (например, библиотеки `requests`), реализация `Varwin.Requests` полностью интегрирована с игровым циклом: каждый запрос является awaitable-объектом и может использоваться в асинхронных цепочках без блокировки выполнения.

Это позволяет естественно встраивать сетевые операции в сценарии поведения:

async def FetchAndReact():
    response = await Varwin.Requests.Get("https://api.example.com/data")
    if response.status_code == 200:
        await cube.ScaleBehaviour.ScaleOverTime(Varwin.Vector3(2, 2, 2), 1)

Varwin.Async.Run(FetchAndReact())

Хотя в некоторых средах выполнения использование сторонних библиотек (включая `requests`) может быть технически возможно, это **не рекомендуется**: синхронные вызовы блокируют основной поток, нарушают плавность симуляции и несовместимы с асинхронной моделью Varwin. Для стабильной и предсказуемой работы всегда используйте `Varwin.Requests`.
