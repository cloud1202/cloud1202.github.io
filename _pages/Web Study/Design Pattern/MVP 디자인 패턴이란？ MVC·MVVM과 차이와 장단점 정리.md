---
title: "MVP 디자인 패턴이란? MVC·MVVM과 차이와 장단점 정리"
date: 2026-07-13
categories: [Web Study, Design Pattern]
tags: [MVP, MVC, MVVM, 디자인 패턴, 소프트웨어 아키텍처, Presenter, Design Pattern]
description: "MVP(Model-View-Presenter) 패턴의 정의와 역사, MVC·MVVM과의 차이, 장단점과 실제 활용 사례를 신뢰할 수 있는 자료를 근거로 정리했습니다. Presenter 계층이 꼭 필요한 이유가 궁금하다면 이 글에서 확인해보세요."
author: OC
is_post: true
thumbnail: "/assets/img/MVP 디자인 패턴이란？ MVC·MVVM과 차이와 장단점 정리/thumbnail.png"
imgAddress: "/assets/img/MVP 디자인 패턴이란？ MVC·MVVM과 차이와 장단점 정리/"
---

## MVP 디자인 패턴 완전 분석

Wikipedia에서는 MVP를 "MVC 아키텍처 패턴의 파생형이며, 주로 사용자 인터페이스 구축에 쓰인다. 자동화된 단위 테스트를 용이하게 하고 프레젠테이션 로직의 관심사 분리를 개선하기 위해 설계됐다"고 설명하고 있다. 나는 이걸 좀 더 풀어서, **View를 최대한 바보로 만들고 그 대가로 로직을 전부 Presenter라는 중간 계층에 몰아넣는 패턴**이라고 이해하고 있습니다. View가 스스로 판단하지 않으니, View 없이도 로직만 따로 떼어 테스트할 수 있다는 게 MVP가 존재하는 이유라고 생각합니다.

MVP는 1990년대 초 애플·IBM·휴렛패커드의 합작사였던 Taligent에서 처음 만들어졌고, C++ 기반 CommonPoint 환경의 개발 모델로 시작해 이후 Java로 이식되었습니다. 이후 Martin Fowler가 이 개념을 정리해 널리 퍼뜨렸고, Microsoft가 2006년 .NET Framework 문서와 예제에 포함시키면서 대중화됐다고 합니다.

![MVP 패턴의 Model-View-Presenter 구조와 데이터 흐름 다이어그램]({{page.imgAddress}}body-1.png)

### MVP를 왜 알아야 하는가?

**바로 답하면, UI 프레임워크에 종속되지 않는 순수 로직을 빠르게 단위 테스트하기 위해서입니다.** iOS를 예로 들면, MVC 구조에서는 UIViewController가 View와 Controller 역할을 동시에 떠안다 보니 화면이 조금만 복잡해져도 네트워킹·영속성·비즈니스 로직·UI 갱신까지 한 클래스에 다 몰리는 "Massive View Controller(비대해진 뷰 컨트롤러)" 문제가 사실상 예정된 결과처럼 나타난다는 지적이 있습니다. MVP는 여기에 Presenter를 끼워 넣어 UIViewController를 View 프로토콜만 구현하는 얇은 계층으로 만들려는 시도로 소개됩니다.

**문제점 요약:** View와 Model, 비즈니스 로직이 한 클래스에 뒤섞이면 UI 프레임워크를 띄우지 않고는 로직 하나 테스트하기가 어려워진다.

**Presenter의 역할:** Model에서 데이터를 가져와 View에 보여줄 형태로 가공하고, View와 Model이 서로를 직접 알지 못하게 중간에서 모든 통신을 전담한다.

GWT(Google Web Toolkit) 공식 문서는 이 차이를 실제 수치로 보여줍니다. 브라우저를 띄워 실행하는 GWTTestCase는 15.23초가 걸린 반면, 같은 로직을 순수 JRE 기반 경량 테스트로 돌리면 0.01초밖에 걸리지 않았다고 합니다. View를 최소화하고 로직을 Presenter로 몰아두면 이 정도로 빠른 테스트 스위트를 만들 수 있다는 게 GWT 팀이 MVP를 채택한 핵심 이유였던 셈입니다.

### Model, View, Presenter는 각각 무엇을 하는가?

Wikipedia 정의를 기준으로 정리하면 이렇습니다.

- **Model**: UI에 표시되거나 조작될 데이터를 정의하는 인터페이스
- **View**: 데이터를 표시하고 사용자의 명령(이벤트)을 Presenter로 전달하는 수동적(passive) 인터페이스
- **Presenter**: Model과 View 둘 다에 작용하며, 저장소(Model)에서 데이터를 가져와 View에 맞는 형태로 가공하는 중간자

안드로이드 구현을 보면 이 역할 분담이 더 명확해집니다. Model은 데이터베이스·네트워크 계층을 포함한 도메인 로직을 담당하고, View(주로 Activity/Fragment)는 사용자 행동을 감지해 Presenter에 알리는 역할만 합니다. 그리고 "하나의 Presenter가 한 번에 하나의 View만 관리"하는 1:1 관계가 원칙이며, 세 요소는 서로 직접 참조하지 않고 반드시 `Contract`라는 인터페이스 묶음(Contract.View, Contract.Model, Contract.Presenter)을 통해서만 통신하도록 설계하는 경우가 많다고 합니다.

![안드로이드 MVP Contract 인터페이스 구조 예시 코드 스크린샷]({{page.imgAddress}}body-2.png)

### MVP와 MVC는 뭐가 다른가?

**핵심 차이는 "누가 중심에 서느냐"입니다.** MVC는 Controller가 Model과 View 양쪽과 통신하는 구조이고, View와 Model이 강하게 결합(tightly coupled)되어 있으며 하나의 Controller가 여러 View를 관리할 수도 있습니다. 반면 MVP는 Presenter가 Model과 View 사이의 모든 통신을 전담하고, Model과 View 사이의 직접 통신은 아예 없습니다. 안드로이드 관점 비교표를 보면 MVC는 계층 간 결합이 강하고 안드로이드 API 의존도도 높은 반면, MVP는 계층 간 결합이 느슨하고 API 의존도가 낮다고 평가됩니다. 테스트 용이성도 MVC는 제한적인 데 비해 MVP는 View-Presenter 결합을 통해 어느 정도 테스트가 가능하다는 차이가 있습니다.

### MVP와 MVVM은 뭐가 다른가?

**연결 방식이 다릅니다.** MVP는 Presenter가 View 인터페이스의 메서드를 직접 호출해 화면을 갱신하는 명시적·수동적 방식이고, MVVM은 ViewModel의 상태를 View가 관찰(observe)하는 선언적 데이터 바인딩 방식입니다. MVVM의 ViewModel은 View를 직접 참조하지 않고 데이터 바인딩과 커맨드를 통해 통신하며, 하나의 ViewModel에 여러 View가 매핑되는 1:다 관계가 가능합니다. 안드로이드 비교표 기준으로는 MVVM이 가장 높은 단위 테스트 용이성과 가장 낮은 프레임워크 의존도를 보인다고 평가되는데, 이는 데이터 바인딩이 View-Model 동기화 코드 자체를 줄여주기 때문입니다.

다만 iOS 쪽 자료는 이 부분을 좀 다르게 짚습니다. 2015년에 작성된 한 유명 비교 글은 "MVP는 iOS에서 뛰어난 테스트 용이성을 주지만 코드량이 많아진다"고 평가하면서, MVP는 View-Presenter 간 바인딩을 수동으로 처리해야 하는 반면 MVVM은 자동 바인딩으로 코드량을 줄인다고 설명합니다. 이 자료는 2015년 기준이라 iOS 생태계가 그 사이 많이 바뀐 점을 감안하고 참고할 필요가 있다고 생각합니다.

![MVC vs MVP vs MVVM 데이터 흐름 비교 표]({{page.imgAddress}}body-3.png)

### Passive View와 Supervising Controller는 무엇이 다른가?

MVP를 좀 더 깊이 파다 보면 반드시 마주치는 개념입니다. Martin Fowler는 원래의 MVP가 사실 서로 다른 두 접근을 뭉뚱그린 것이었다고 판단해, 2006년 7월 11일 이를 **Supervising Controller**와 **Passive View**라는 두 패턴으로 공식 분리했습니다.

- **Supervising Controller**: 컨트롤러(프레젠터)는 최대한 아무것도 하지 않는 게 목표입니다. 단순한 View-Model 동기화는 데이터 바인딩에 맡기고, 복잡한 로직이 있을 때만 개입합니다. 그만큼 매핑 코드가 적습니다.
- **Passive View**: 위젯을 매핑조차 없는 완전히 수동적인 존재로 만들어, 남아있던 작은 위험까지 제거합니다. 대신 모든 View 갱신이 컨트롤러 쪽으로 넘어가니 코드량은 늘고, 테스트할 때는 화면을 흉내내는 테스트 더블(Test Double)이 필요합니다.

두 변형 다 나름의 트레이드오프를 감수하는 절충안이라, "정답"이 하나로 정해져 있다기보다는 프로젝트 상황에 맞춰 고르는 문제라고 생각합니다.

### MVP는 실제로 어디에 쓰이는가?

MVP는 .NET(Windows Forms, ASP.NET), Java 진영(Swing, JavaFX, GWT, Vaadin), PHP 프레임워크(Laravel, CodeIgniter) 등 여러 플랫폼에서 채택된 이력이 있습니다. 특히 GWT는 클라이언트 사이드 싱글 페이지 애플리케이션을 구조화하는 공식 아키텍처로 MVP를 채택하면서, Presenter가 이벤트 처리·원격 서비스 데이터 조회·히스토리 관리·화면 전환까지 로직 전체를 담당하도록 설계했다고 합니다. 안드로이드 개발사 Infinum의 사내 기술 핸드북도 "views, presenters, interactors, listeners" 패키지 구조로 MVP를 나누고, Dagger2 같은 의존성 주입 도구로 컴포넌트를 연결하는 방식을 실무 예제로 제시한 바 있습니다.

![MVP를 채택한 대표 플랫폼 예시 - GWT, Vaadin, 안드로이드 아이콘 나열]({{page.imgAddress}}body-4.png)

### MVP의 한계와 트레이드오프는 무엇인가?

여기서부터는 장점만 늘어놓지 않고 짚고 넘어가야 할 부분입니다. MVP에는 내장된 데이터 바인딩이 없기 때문에 UI 갱신을 전부 수동으로 처리해야 하고, 복잡한 UI 상호작용에서는 유연성이 떨어지며 안드로이드 컴포넌트 통합에 더 많은 수작업이 필요할 수 있습니다. 또 단일 책임 원칙을 제대로 지키지 않으면 Presenter 계층이 점점 커져서 "모든 것을 아는 거대한 클래스"가 되어버리는 경향이 있다는 지적도 있습니다.

iOS 쪽에서는 View가 Model을 알아서는 안 되기 때문에 이 둘을 초기화(assembly)해줄 별도 지점이 필요한 "조립 문제(assembly problem)"가 발생한다는 평가도 있는데, 이 내용 역시 2015년 자료 기준이라 현재 iOS 생태계에 그대로 적용되는지는 조심스럽게 받아들일 필요가 있습니다. 앞서 언급한 Passive View와 Supervising Controller의 트레이드오프(테스트 더블 필요 vs 검증되지 않는 바인딩 로직)도 결국 MVP를 쓰는 순간 감수해야 하는 비용이라고 봅니다.

## MVP, 실무에서는 언제 고려할 만한가

MVP를 정리하면서 느낀 건, 이 패턴이 "무조건 좋다"거나 "이미 한물갔다"고 딱 잘라 말하기엔 자료마다 온도차가 꽤 있다는 점입니다. Infinum의 안드로이드 핸드북은 MVP 문서를 "(deprecated)"로 명시하며 "안드로이드 팀은 MVP를 넘어섰고 이제 모든 신규 프로젝트에 MVVM을 쓰고 있다"고 밝혔고, daily.dev 블로그도 신규 프로젝트나 리팩터링이라면 MVVM 구조를 확인하라고 권장합니다. 한 자료는 개발자 설문 결과로 "약 37%가 데이터 바인딩 때문에 MVVM을 선호하고, 약 27%는 여전히 단순한 구현과 View 계층에 대한 강한 통제력 때문에 MVP를 선호한다"는 수치를 인용하는데, 이 설문의 출처와 조사 시점이 명확히 특정되지 않아 수치를 곧이곧대로 최신 트렌드로 받아들이기보다는 "MVP를 여전히 선호하는 개발자층이 소수지만 존재한다" 정도의 참고 자료로 보는 게 맞다고 생각합니다.

### 1. 테스트 우선순위가 높은 프로젝트라면

GWT 사례처럼 브라우저·프레임워크 의존성 없이 빠른 단위 테스트 스위트를 만들고 싶다면 MVP의 구조 자체가 여전히 유효한 선택지라고 봅니다. Presenter만 떼어내서 테스트할 수 있다는 장점은 MVVM이 등장했다고 사라지는 게 아니기 때문입니다.

### 2. 데이터 바인딩이 없거나 레거시를 유지보수해야 한다면

daily.dev나 GeeksforGeeks 자료를 종합하면, 검색 결과상으로 구글의 최신 가이드라인은 MVVM을 명확히 선호하는 쪽이지만 MVP가 "공식적으로 폐기"된 것은 아니고, 주로 레거시 코드베이스 유지보수와 관련이 깊다고 정리됩니다. 이미 MVP로 짜인 코드베이스를 이어받았거나, 데이터 바인딩 기능이 없는 프레임워크(PHP 진영 등)에서 작업한다면 굳이 MVVM으로 갈아엎기보다 MVP 원칙을 그대로 따라가는 게 현실적일 수 있습니다.

---

## 결론 및 실무적 고려 사항

정리하면, MVP는 View를 수동적으로 만들고 Presenter에 로직을 몰아 UI 프레임워크 의존 없이 빠르게 테스트할 수 있게 해주는 패턴입니다. MVC보다 결합도가 느슨하고, MVVM보다는 명시적인 방식으로 View-Model을 연결한다는 게 세 패턴을 가르는 핵심 축이라고 정리할 수 있습니다.

다만 데이터 바인딩이 없어 UI 갱신을 손으로 다 챙겨야 한다는 점, Presenter가 방치되면 거대한 클래스가 되기 쉽다는 점, Passive View/Supervising Controller 두 변형 모두 나름의 대가를 요구한다는 점은 분명한 한계입니다. 신규 프로젝트라면 MVVM을 먼저 검토하되, 레거시 유지보수나 데이터 바인딩이 없는 환경, 혹은 테스트 용이성이 최우선인 상황이라면 MVP도 여전히 현실적인 선택지라고 생각합니다. 결국 어떤 패턴을 쓰느냐보다 "View를 어디까지 수동적으로 둘 것인가"라는 질문에 팀이 먼저 답을 정하는 게 순서라고 봅니다.

---
*참고:*
- [Model–view–presenter - Wikipedia](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93presenter)
- [Retirement note for Model View Presenter Pattern - Martin Fowler](https://martinfowler.com/eaaDev/ModelViewPresenter.html)
- [Supervising Controller - Martin Fowler](https://martinfowler.com/eaaDev/SupervisingPresenter.html)
- [Building MVP apps: MVP Part I - GWT 공식 문서](https://www.gwtproject.org/articles/mvp-architecture.html)
- [Difference Between MVC, MVP and MVVM Architecture Pattern in Android - GeeksforGeeks](https://www.geeksforgeeks.org/android/difference-between-mvc-mvp-and-mvvm-architecture-pattern-in-android/)
- [MVP Architecture Pattern in Android with Example - GeeksforGeeks](https://www.geeksforgeeks.org/android/mvp-model-view-presenter-architecture-pattern-in-android-with-example/)
- [Infinum Handbook - MVP (deprecated)](https://infinum.com/handbook/android/project-architecture/mvp-deprecated)
- [iOS Architecture Patterns - Bohdan Orlov, Medium (2015-11-28)](https://medium.com/ios-os-x-development/ios-architecture-patterns-ecba4c38de52)
- [iOS Architecture Showdown - Sachindra Fernando, Medium](https://medium.com/@sachindrafernando3/ios-architecture-showdown-mvc-mvp-mvvm-viper-explained-f7a90319c424)
