# Varwin Python-скрипты

Проект — скрипты на Python для **Varwin 18** (XRMS / Education + расширение «Varwin Python»).
Полный справочник API: `docs/varwin18_python_api_full.md` (снят с scripting.varwin.com/18/ru, декабрь 2025).
Сайты varwin.com блокируют прямой доступ; обновлять можно через `https://r.jina.ai/https://scripting.varwin.com/18/ru/<page>`.

## Как устроен проект в Varwin

```
Blockly.py            # read-only, генерится из блоков
Main.py               # РЕДАКТИРУЕМЫЙ, точка входа
<свои модули>.py      # редактируемые, импортируются из Main.py
Varwin/Varwin.py      # read-only, API
Varwin/SceneObjectTypes.py  # read-only, алиасы типов (XxxWrapper)
Varwin/SceneObjects.py      # read-only, переменные объектов сцены
```

Объект сцены доступен по «Имени переменной» из редактора сцены: `from SceneObjects import *` → `cube1`, `player`, ...

## Шаблон Main.py

```python
import Varwin
from SceneObjects import *
from SceneObjectTypes import *   # нужно для enum-ов обёрток: PlayerWrapper.MovementType...
import Blockly                    # оставить, если в проекте есть логика на блоках

async def OnStart():
    pass

async def OnUpdate():   # каждый кадр — ничего тяжёлого и ничего долгого
    pass

Varwin.Async.AddStart(OnStart)    # передаём ФУНКЦИЮ, не вызов
Varwin.Async.AddUpdate(OnUpdate)
```

## Жёсткие правила

- Весь код — в главном потоке движка. **Нельзя**: `asyncio`, `threading`, `time.sleep`, `requests` (блокируют кадр).
- Задержки: `await Varwin.WaitForSeconds(s)`, `await Varwin.WaitWhile(lambda: cond)` (ждёт, пока cond == True), `Varwin.WaitForEndOfFrame()`.
- Параллельные цепочки: `Varwin.Async.Run(coro())` — передаётся ВЫЗОВ корутины.
- `AddStart/AddUpdate` и все `Add*Handler` принимают саму функцию. Обработчики пишем `async def`.
- У обработчиков событий последний аргумент всегда `sender` (объект, вызвавший событие).
- Методы с пометкой async в API (`MoveByAxisAtDistance`, `ScaleOverTime`, `PlaySound`, ...) нужно `await`-ить, иначе движение/действие запустится без ожидания.
- HTTP — только `await Varwin.Requests.Get/Post/Put/Delete(url, *, params=|data=|json=, headers=)` → `resp.status_code`, `resp.text`, `resp.content`.
- Enum-значения — атрибуты вложенных классов: `Varwin.PhysicsBehaviour.GravityState.Off`, `VBotBoyWrapper.MovementPace.Run`. Значение Python-ключевого слова `None` пишется `None_`.
- Логи: `Varwin.Debug.Log / LogWarning / LogError`.

## Шпаргалка API (подробности — в docs/)

**Varwin.Object** (любой объект сцены): `GetName() GetTypeName() GetParent() GetChildren() GetDescendants() GetAncestry()`,
`Enable() Disable() Activate() Deactivate() IsActive() IsInactive() IsEnabled() IsDisabled()`, props `Activity Enabled`,
`TransformPoint(v) InverseTransformPoint(v)`, поведения: `.MotionBehaviour .RotateBehaviour .ScaleBehaviour .PhysicsBehaviour .InteractionBehaviour .VisualizationBehaviour`.

**MotionBehaviour**: `TeleportTo(obj) SetPosition(v) MoveByAxisWithSpeed(axisVec, speed)`, async: `MoveByAxisAtDistance(axisVec, dist, speed) MoveByAxisOverTime(axisVec, dur, speed) MoveToObjectAtSpeed(obj, speed) MoveToCoordinatesAtSpeed(v, speed) MoveAlongThePath([obj|v...], speed)`,
`Stop Pause Continue IsMovingNow GetDistanceToObject(obj) GetDistanceToVector(v)`, props `Position PositionX/Y/Z MovementFaceDirection MinimumTargetStopDistance`,
events `AddMovementFinishedHandler(s) AddToWrapperMovementFinishedHandler(target,s) AddToVectorMovementFinishedHandler(v,s) AddWaypointReachedHandler(idx,point,s)`.

**RotateBehaviour** (Axis.X/Y/Z, RotationAxis.All/LocalX/LocalY): `SetRotation(euler) RotateAroundAxis(angle, Axis) RotateToObjectAroundAxis(obj, RotationAxis) RotateAsObject(obj) RotateAroundAxisWithSpeed(Axis, speed) RotateAroundAnotherObjectAxisWithSpeed(Axis, obj, speed)`,
async: `RotationAroundAxisWithSpeedOverTime(Axis, time, speed) LookAtObjectWithSpeedAroundAxis(obj, speed, RotationAxis) RotateAsObjectWithSpeed(obj, speed) RotateToVectorWithSpeed(v, speed) RotateAroundAxisByAngleWithSpeed(Axis, angle, speed)`,
`Stop Pause Continue IsRotatingNow AngleX() AngleY() AngleZ() GetRotationAroundAxisToObject(Axis,obj) GetRotationToObject(obj)`, prop `Angle`,
events `AddRotationFinishedHandler AddToWrapperRotationFinishedHandler AddAsWrapperRotationFinishedHandler AddToVectorRotationFinishedHandler`.

**ScaleBehaviour**: `SetScale(v)`, async `ScaleOverTime(v, t) ScaleByFactorOverTime(k, t)`, `Stop Pause Continue IsScalingNow`, props `Scale ScaleX/Y/Z`, `AddScalingFinishedHandler`.

**PhysicsBehaviour** (Relativeness.Self/World, GravityState.On/Off, KinematicState.Kinematic/NonKinematic, ObstacleState.Obstacle/NonObstacle):
`ApplyForceInDirection(force, dirVec, Relativeness)`, async `StartApplyingForceInDirectionRelativeTo(force, dirVec, dur, Relativeness)`, `Pause Continue Stop IsAffectedByForceNow`,
props `Mass Bounciness Gravity LinearDrag AngularDrag Acceleration Speed AngularSpeed Kinematic Obstacle`, `AddApplicationOfForceCompletedHandler`.

**InteractionBehaviour** (ControllerHand.None_/Left/Right; *State.Enabled/Disabled): `IsTouching IsUsing IsGrabbed`, props `CanTeleport CanTouch CanUse CanGrab`,
events `AddTouchStarted/EndedHandler(s)`, `AddUseStarted/EndedHandler(hand,s)`, `AddGrabStarted/EndedHandler(hand,s)`.

**VisualizationBehaviour**: `ChangeObjectColor(color)`, async `ChangeColorOverTime(color, t)`, `SetChangingColorState(PlayableState.Stop/Pause/Continue) IsColorChangingNow`, prop `Color`.

**Статические модули Varwin**:
- `Vector3(x,y,z)`: `.X .Y .Z .Normalized .Magnitude`, `Dot Cross Distance Rotate(v, euler)`.
- `Color(r,g,b,a)` 0..1: `FromHex("#..") GetRandom() Lerp(a,b,t)`.
- `Objects`: `GetAll() GetObjectsOfType(VCubeWrapper) GetObjectByInstanceId(id) GetObjectByVarName("name")`.
- `Cloning`: `Clone(o) CloneAtPosition(o, v) CloneAtObjectPosition(o, target) Destroy(clone) DestroyAllClones(o) GetClones(o) IsClone(o) IsCloneOfObject(c, orig) IsDestroyed(o)`.
- `Collisions.AddCollisionStartHandler / AddCollisionEndHandler`: `(handler)` или `(first, second, handler)`, где first/second — объект или список; handler `(a, b)`.
- `Project`: `RestartScene() LoadSceneByName/Guid LoadConfigurationByName/Guid`, `AddPrepareSceneHandler`, `AddPlatformChangedToVR/AR/Desktop/NettleDeskHandler`.
- `Random`: `RandInt(a,b) RandFloat(a,b) TrueWithProbability(p)`. `Math.IsPrime(n)`. `StringUtils`: `GetLineBreak Replace GetRandomLetter`. `ListUtils`: `FirstIndex LastIndex` (0 = не найдено → индексация с 1, как в Blockly).
- `Application.OpenUrl(url)`, `DynamicValueDictionary.Get(id)`, `Variable` (`.Value`, `AddValueChangedHandler(old,new)`), `Range(start, stop, step)`.

**Обёртки базового контент-пака** (тип = `<Имя>Wrapper`, наследуют Object):
- `PlayerWrapper` — перемещение (`AllowMovementType/ProhibitMovementType(MovementType.*)`, `TeleportToObject/Vector/StartPosition`, async `MoveToPointWithSpeed/MoveToObjectWithSpeed`), повороты, `ForceGrab*/ForceDrop*`, вибрация, `AttachCameraToObject`, проверки `CheckObjectIn*Hand`, props `WalkingSpeed SprintSpeed JumpHeight HeadPosition HeadRotation ...`, events `AddAnyHandCollidedHandler(hand,obj,s)`, `AddControllerEnabled/DisabledHandler`.
- `VBotBoyWrapper / VBotGirlWrapper` — `SayText SayTextWith StopSpeaking`, async `MoveByMeters MoveToObject MoveAlongPath RotateByAngle`, `MoveInfinite StopMovement PausePath ContinuePath`, events `AddBotTargetReachedHandler AddBotPathPointReachedHandler AddSpeechCompletedHandler`.
- `VTextWrapper` — `SetText GetText`, props `TextColor PanelColor Size Font Bold ...`. `TutorialDisplayWrapper.SetText`.
- `TutorialButtonWrapper` — `IsPressed SetPressedState SetReleasedState AddPressedHandler AddReleasedHandler`. `TutorialBulbWrapper` — `TurnOn TurnOff IsOn`, prop `Color`.
- `CustomZoneWrapper` — `IsContainObject GetContainedObjects AddObjectEnteredHandler(obj,s) AddObjectExitedHandler(obj,s)`.
- `VarwinAudioWrapper` — async `PlaySound StopSound PauseSound`, `Seek IsPlaying IsPaused IsStopped`, props `Volume Speed Length CurrentTime PlaybackLoopState`, `AddPlaybackCompletedHandler`.
- `VarwinVideo(180/360)Wrapper` — async `LoadAndPlay Pause Stop`; `StreamingVarwinVideo*` — `Play Pause Stop` (синхронные). `VarwinModelWrapper` — анимации. `VPanorama*`, свет `VDirectional/Point/SpotLight`, `VSmileWrapper`, `SKJoystick/SKFlyingDrone/SKHumanoidBot/SKSimpleBot`, `ARMarkerWrapper`, `Basketball_HoopWrapper.AddRingHitHandler`.
- Примитивы без своих методов: `VCube VSphere VCylinder VCone VPlane VPyramid VHexagon VEmptyObject`, коллайдеры.

## Неясности в документации (проверять в Varwin при первом запуске)

- Сеттеры свойств (`obj.PhysicsBehaviour.Mass = 2`, `text.TextColor = ...`) в доках не показаны явно, но подразумеваются.
- На странице примеров часть методов вымышленная (`valve.IsOpen`, `door.Lock`, `hint_ui.Show`) и обработчик написан через `def` — ориентироваться на справочник API, а не на примеры.
- Доступ к переменным Blockly из Python (`Varwin.Variable`) — через модуль `Blockly`, точный путь не задокументирован.
- Сторонние pip-библиотеки заявлены маркетингом (TensorFlow, PyTorch), способ установки не описан.
