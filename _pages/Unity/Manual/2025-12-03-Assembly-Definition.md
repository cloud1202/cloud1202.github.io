---
title: "Unity Assembly Definition 활용"
tags:
    - Unity
date: "2025-12-03"
thumbnail: "/assets/img/thumbnail/book.jpg"
imgAddress: "/assets/img/2025-12-03-Assembly-Definition/"
description: "Unity Assembly Definition(.asmdef) 정리. UIManager와 PlayerManager가 서로를 참조하던 순환참조를 실제 코드로 재현하고, asmdef 파일 구성과 이벤트 기반 구조로 단방향 의존성을 만든 과정, 컴파일 속도 변화까지 기록했습니다."
is_post: true
featured: true
---
## 🚀 Unity 개발 필수: Assembly Definition File (.asmdef) 완전 분석

[**Unity Document**](https://docs.unity3d.com/kr/2023.2/Manual/ScriptCompilationAssemblyDefinitionFiles.html)에서는 아래와 같이 설명해주고 있다.
!["Default_View.png"]({{page.imgAddress}}UnityDocument.png "유니티 기본 구성화면")

**Assembly**란 메인 기능이 같은 코드를 묶어 그룹화 했다고 나는 이해하고 있다. 이는 컴파일 시 하나의 **DLL(Dynamic Link Library)** 파일로 만들어지는 논리적인 코드 묶음 단위이다.
Unity는 별도의 설정이 없다면 위 이미지와 같이 **Assembly-CSharp** 하나에 모든 코드를 통합하여 관리하게 된다.
이를 사용자 편의에 맞춰 각 기능별로 **모듈화** 시켜주는 작업을 **Assembly Definition File (.asmdef)**을 활용하여 진행하면 된다.

### 왜 써야 하는가?

**Assembly-CSharp**에 모든 코드가 통합되어 묶여 있는 상황에서는, `UIManager`와 `PlayerManager`처럼 서로 다른 기능을 가진 모듈들이 서로를 직접 참조하는 상황이 비정상적으로 보이지 않을 수 있습니다. 오히려 에러 없이 원하는 기능을 쉽게 호출할 수 있어 일견 편리하게 느껴질 수도 있죠.

하지만 프로젝트 규모가 커질수록 이러한 **'쉬운 참조'**가 낳는 문제점들이 드러나기 시작합니다.

나는 **UI 관련 코드**만 수정했는데, Unity는 **몬스터**와 관련된 코드까지 모두 검사하며 컴파일하고 있습니다. 몬스터와 관련된 기능은 전혀 건드리지도 않았는데 말이죠. 

더 나아가, UI 관련 코드만을 **독립적으로 분리하여 테스트**하고 싶을 때 수많은 에러가 발생합니다. `몬스터를 찾을 수 없고`, `플레이어를 찾을 수 없고`, `무기를 찾을 수 없다`고 합니다. 나는 그저 UI에 나타나는 텍스트를 수정하려고 했을 뿐인데...

이러한 **높은 결합도(High Coupling)**와 **비효율적인 컴파일**이라는 근본적인 이상함을 느꼈다면, 코드를 기능별로 명확하게 분리하는 **Assembly Definition File (.asmdef)**을 활용해야 할 때입니다.

아래는 `.asmdef` 기능을 사용할 때 얻을 수 있는 핵심적인 이점
```
1. 쌍방향 참조 제한 (낮은 결합도 유도)
2. 컴파일 속도 증가 (점진적 컴파일)
```

#### 1. 쌍방향 참조(Circular Dependency) 제한
쌍방향 참조란 서로가 서로를 참조하는 상황을 말하며, 이는 모듈 간의 **높은 결합도(High Coupling)**를 유발하여 테스트와 유지보수를 어렵게 만듭니다.

예를 들어, UIManager와 PlayerManager 라는 Manager 클래스가 있다고 가정할 때 각 Manager의 기능은 아래와 같다.
UIManager : 플레이어 체력 표시, 인벤토리 표시 등
PlayerManager : 플레이어 정보 보유, 데미지 판정 기능 등

위와 같을 때, 몬스터 A가 플레이어를 공격 하면 PlayerManager는 데미지가 들어왔다고 판단하여 UIManager를 호출하여 플레이어 체력을 감소 시켜 줍니다.
그러고 플레이어가 인벤토리에서 체력 포션을 사용하게 되면 UIManager는 PlayerManager를 호출하여 체력이 회복되었다고 알려줍니다.

**👉 문제점 요약:**
이렇게 되면 `UIManager`와 `PlayerManager`는 메인 기능이 서로 다름에도 불구하고 서로를 참조하게 됩니다. 이로 인해 `UIManager`의 일부 기능(예: 메인메뉴)만 테스트하고 싶어도 전체 시스템(`PlayerManager` 포함)을 로드해야 하는 **독립성 저하** 문제가 발생합니다.

**✅ .asmdef의 역할:**
**.asmdef** 파일을 사용하면, 각 어셈블리(모듈) 간의 **참조 관계**를 파일 내에서 **명시적**으로 정의해야 합니다. 이 과정에서 A가 B를 참조하고, B가 A를 참조하는 **의도치 않은 순환 참조**를 **컴파일 단계에서부터 차단**하여, 개발자가 처음부터 **단방향 의존성**을 설계하도록 강제합니다.

**📄 실제로 어떤 코드였나**

말로만 보면 감이 잘 안 오니, 위 상황을 코드로 옮겨봤습니다.

```csharp
// Assets/Scripts/Player/PlayerManager.cs
public class PlayerManager : MonoBehaviour
{
    public static PlayerManager Instance;

    public int Hp { get; private set; } = 100;

    public void TakeDamage(int amount)
    {
        Hp -= amount;
        UIManager.Instance.UpdateHpBar(Hp);   // (1) Player -> UI 직접 호출
    }

    public void Heal(int amount)
    {
        Hp = Mathf.Min(Hp + amount, 100);
        UIManager.Instance.UpdateHpBar(Hp);
    }
}
```

```csharp
// Assets/Scripts/UI/UIManager.cs
public class UIManager : MonoBehaviour
{
    public static UIManager Instance;

    [SerializeField] private Slider hpBar;

    public void UpdateHpBar(int hp)
    {
        hpBar.value = hp / 100f;
    }

    // 인벤토리에서 체력 포션을 눌렀을 때
    public void OnClickPotion()
    {
        PlayerManager.Instance.Heal(30);      // (2) UI -> Player 직접 호출
    }
}
```

(1)과 (2). 이게 순환 참조입니다.
**하나의 `Assembly-CSharp`에 다 들어 있을 땐 이 코드가 아무 에러도 내지 않습니다.**
컴파일도 잘 되고 게임도 잘 돌아갑니다. 그래서 문제라는 자각조차 없었습니다.

여기에 `.asmdef`를 얹는 순간 이야기가 달라집니다.
`Game.Player`는 `UIManager`를 쓰니 `Game.UI`를 참조해야 하고,
`Game.UI`는 `PlayerManager`를 쓰니 `Game.Player`를 참조해야 합니다. 그 결과:

```text
Assembly with name 'Game.UI' has cyclic references
```

**컴파일이 아예 안 됩니다.** 잘 돌아가던 코드가 갑자기 막히니 처음엔 당황스러웠는데,
사실은 원래부터 있던 설계 문제를 컴파일러가 뒤늦게 잡아준 것이었습니다.

#### 2. ⚡️ 컴파일 속도 증가 (점진적 컴파일)
Unity에서는 코드를 수정하게 되면 컴파일러에 의해 컴파일을 한번 거치게 된다. 이 과정은 문법 에러나, 참조 에러를 발견해 사용자에게 알려주는 중요한 단계이다.

**❌ .asmdef 미사용 시 (문제점):**
문제는 내가 A라는 `.cs` 파일을 수정했을 때 동일한 **Assembly-CSharp** 내의 **모든 코드**를 통째로 컴파일 하게 되어서, 묶여있는 코드들이 많을수록 컴파일 시간이 기하급수적으로 늘어나게 된다.
수정하고 테스트 하는 것이 일상인 개발자에게 이는 꽤나 큰 시간 낭비로 다가왔고, 특히 팀 프로젝트 규모가 커질수록 이 문제는 더욱 심각해진다.

**✅ .asmdef 사용 시 (해결책):**
**.asmdef**를 사용하면 프로젝트의 코드가 여러 개의 작은 **독립적인 어셈블리**로 분할됩니다. 이제 A라는 파일 하나를 수정하더라도, 컴파일러는 **A가 속한 어셈블리**와 **A 어셈블리를 참조하는 다른 어셈블리**만 재컴파일(Recompile)합니다. 나머지 독립된 어셈블리는 컴파일하지 않아 **컴파일 시간이 획기적으로 단축**됩니다.

----

## ✅ Assembly Definition (.asmdef) 개인 프로젝트 적용 후기

실제로 기능을 경험해보고자 개인 프로젝트에 **Assembly Definition File (.asmdef)**을 적용해 보았습니다.
이 기능이 주로 **대규모 팀 프로젝트**에서 빛을 발한다는 이야기를 많이 들었지만, 처음부터 큰 프로젝트에 적용하는 것은 어려울 것이라 판단하여 작은 프로젝트에서 경험을 시작했습니다.

적은 코드였음에도 **불필요하고 복잡한 참조**가 많았고, 이 참조들을 제거하고 모듈화하는 과정에서 **객체 지향 설계 능력**이 향상되는 듯한 착각을 느꼈습니다.

### 1. 🤝 결합도 감소 및 단방향 의존성 확립

위에 적은 이점대로 어셈블리 간의 **불필요한 직접 참조**가 사라졌음을 체감했습니다.

가장 큰 변화는 **이벤트 기반 시스템** 도입입니다. 예를 들어, 몬스터가 죽으면 점수가 올라가는 로직이 있다고 가정해 봅시다.
* **이전 (직접 참조):** `Monster.cs`에서 `Score.cs`에 있는 점수 증가 함수를 **직접 호출**했습니다. (쌍방향 참조 유발)
* **현재 (이벤트 기반):** `Monster.cs`는 `GameManager`(공통 클래스)에 **몬스터가 죽었다는 신호(이벤트)**만 보냅니다. `Score.cs`는 이 이벤트를 구독하고 있다가 신호가 오면 자신의 점수를 올리는 함수를 실행합니다.

```text
   Game.UI                         Game.Player
  (Score.cs)                      (Monster.cs)
      |                                |
      | 이벤트 구독                     | 이벤트 발생
      |                                |
      +----------> Game.Core <---------+
                 (GameEvents)

  - UI와 Player는 서로를 전혀 모른다
  - 둘 다 Game.Core 한 방향만 참조한다 (단방향 의존성)
```

**📄 앞의 순환참조 코드를 이렇게 바꿨습니다**

먼저 양쪽이 공통으로 참조할 최하위 어셈블리(`Game.Core`)에 이벤트만 모아둡니다.

```csharp
// Assets/Scripts/Core/GameEvents.cs   (어셈블리: Game.Core)
public static class GameEvents
{
    public static event Action<int> OnPlayerHpChanged;
    public static event Action OnPotionUsed;

    public static void RaiseHpChanged(int hp) => OnPlayerHpChanged?.Invoke(hp);
    public static void RaisePotionUsed() => OnPotionUsed?.Invoke();
}
```

`PlayerManager`는 이제 UI를 부르지 않고 "체력이 바뀌었다"고 알리기만 합니다.

```csharp
// 어셈블리: Game.Player  (references: Game.Core)
public class PlayerManager : MonoBehaviour
{
    public int Hp { get; private set; } = 100;

    private void OnEnable()  => GameEvents.OnPotionUsed += HandlePotionUsed;
    private void OnDisable() => GameEvents.OnPotionUsed -= HandlePotionUsed;

    public void TakeDamage(int amount)
    {
        Hp -= amount;
        GameEvents.RaiseHpChanged(Hp);       // UIManager를 몰라도 된다
    }

    private void HandlePotionUsed()
    {
        Hp = Mathf.Min(Hp + 30, 100);
        GameEvents.RaiseHpChanged(Hp);
    }
}
```

`UIManager`도 마찬가지로 `PlayerManager`를 모릅니다.

```csharp
// 어셈블리: Game.UI  (references: Game.Core)
public class UIManager : MonoBehaviour
{
    [SerializeField] private Slider hpBar;

    private void OnEnable()  => GameEvents.OnPlayerHpChanged += UpdateHpBar;
    private void OnDisable() => GameEvents.OnPlayerHpChanged -= UpdateHpBar;

    private void UpdateHpBar(int hp) => hpBar.value = hp / 100f;

    public void OnClickPotion() => GameEvents.RaisePotionUsed();
}
```

> `OnEnable` / `OnDisable` 짝을 꼭 맞춰야 합니다.
> `static` 이벤트는 씬을 바꿔도 살아남기 때문에, 해제를 빼먹으면
> 파괴된 오브젝트를 붙잡고 있다가 `MissingReferenceException`이 납니다.
> 순환 참조를 없애는 대신 **구독 해제 책임**이 새로 생긴 셈입니다.

**⚙️ .asmdef 파일은 이렇게 생겼습니다**

Inspector에서 체크박스로 만지는 게 전부지만, 실제 저장되는 건 평범한 JSON입니다.

```json
// Assets/Scripts/Player/Game.Player.asmdef
{
    "name": "Game.Player",
    "rootNamespace": "Game.Player",
    "references": [
        "Game.Core"
    ],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "precompiledReferences": [],
    "autoReferenced": true,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false
}
```

핵심은 `references` 한 줄입니다. 여기에 적히지 않은 어셈블리의 코드는
**같은 프로젝트 안에 있어도 컴파일 단계에서 보이지 않습니다.**
`Game.Player`의 `references`에 `Game.UI`가 없으므로, 실수로 `UIManager.Instance`를 치면
그 자리에서 바로 빨간 줄이 그어집니다.

**한 줄 요약: 적용 전/후**

| | 적용 전 | 적용 후 |
|---|---|---|
| 어셈블리 | `Assembly-CSharp` 하나 | `Game.Core` / `Game.Player` / `Game.UI` |
| Player -> UI | `UIManager.Instance.UpdateHpBar()` 직접 호출 | `GameEvents.RaiseHpChanged()` 이벤트 발행 |
| UI -> Player | `PlayerManager.Instance.Heal()` 직접 호출 | `GameEvents.RaisePotionUsed()` 이벤트 발행 |
| 잘못된 참조 | 에러 없음 (돌아는 감) | **컴파일 에러로 즉시 차단** |
| 재컴파일 범위 | 전체 코드 | 수정한 어셈블리 + 그걸 참조하는 어셈블리 |

### 2. ⚡️ 컴파일 속도 향상 (점진적 컴파일)

프로젝트 규모가 작아 컴파일 속도가 와닿지 않을 것이라고 생각했지만, 변화를 체감할 수 있었습니다.

이전에는 코드를 수정하면 프로젝트의 **모든 코드**가 묶인 하나의 거대한 **Assembly-CSharp**를 재컴파일하느라 **일정 시간 지연**이 발생했습니다.

`.asmdef` 적용 후에는, **참조하는 어셈블리가 적은 모듈 (작은 .dll)**을 수정했을 때 컴파일 시간이 눈에 띄게 줄어들었습니다. 이는 수정된 파일과 그에 의존하는 어셈블리만 컴파일하는 **점진적 컴파일(Incremental Compilation)**이 정상적으로 작동함을 의미합니다. 작은 프로젝트에서도 개발 효율성이 올라감을 확인할 수 있었습니다.

----

## 💡 결론 및 실무적 고려 사항

작은 프로젝트임에도 불구하고 `.asmdef`가 제공하는 **결합도 감소**와 **컴파일 속도 개선** 이점을 모두 체감했습니다.

하지만 동시에, **큰 프로젝트일수록 적용하기 더 어려울 수 있다**는 생각도 들었습니다. 관리할 코드가 많아지고 팀원이 많아질수록
* **초기 설계의 어려움:**  모든 코드를 나누고 참조 관계를 정의하는 초기 설정 비용이 높습니다.
* **유지보수의 어려움:**  모듈 간의 참조 규칙을 지키기 위한 **팀 내 규칙 정립** 및 이를 일관되게 관리할 **전담 역할**이 필요하다는 것을 느꼈습니다.

결론적으로, `.asmdef`는 단순한 '속도 개선'을 넘어, **코드 설계 능력**과 **개발 능률**을 동시에 끌어올리는 강력한 도구입니다. 작은 규모에서부터 습관을 들이는 것이 가장 중요하다고 생각합니다.