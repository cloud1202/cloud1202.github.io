---
layout: post
title: Unity 구성 화면(Scene, Game, Hierarchy, Inspector, Project)
tags: Unity
date: 2022-08-24 15:10 +0900
category: Unity
toc: true
---
## Unity 기본 구성화면
**Unity**의 기본 구성화면은 아래와 같이 되어있다.
!["Default_View.png"](/assets/img/2022-08-24-Unity-View/All_View.png "유니티 기본 구성화면")  

### Hierarchy View
이미지의 1번에 해당하는 **Hierarchy View**는 추후 설명될 **Scene View**에 있는 오브젝트들의 리스트를 보여주는 창으로 **계층 창** 이라고도 한다.  
오브젝트의 부모, 자식관계를 볼 수 있고, 오브젝트의 생성, 삭제, 복제 등 개발자가 수동으로 오브젝트의 관리를 할 수 있도록 해준다.  
<br><u>자주 사용하는 단축키</u>  
`Ctrl + D` : 오브젝트를 선택후 해당 단축키를 사용하면 오브젝트가 복사된다.  
`Del` : 오브젝트를 선택후 해당 단축키를 사용하면 오브젝트가 삭제된다.  
`Ctrl + A` : 전체 오브젝트를 선택한다.

### Scene / Game View
 - Scene View :  
 이미지의 2번에 해당하는 **Scene View**는 오브젝트를 시각화 해주는 창이다.  
왼손 좌표계를 기준으로 오브젝트들을 시각화 할 수 있고, 이동, 변형, 회전 등의 작업이 가능하며, 마우스의 드래그를 사용하여 오브젝트를 선택할 수 있다.  
카메라와 빛, 배경 이미지 등을 설정하여 **Game View**에서 확인이 가능하다.  
**Hierarchy View**에 있는 오브젝트를 더블 클릭하는 경우 해당 오브젝트를 **Scene View** 정중앙에 배치하는 구도로 이동한다.  
<br><u>자주 사용하는 단축키</u>  
`우클릭` : Secen View의 화면 앵글을 회전시켜준다.  
`Alt + 우클릭` : 현재 마우스 커서 위치를 기준으로 확대/축소 한다. (상, 좌로 드래그 시 축소, 하, 우로 드래그 시 확대)  
`W / A / S / D + 우클릭` : Scene View의 화면 위치를 현재 보는 방향 기준에서 이동한다. (우클릭 드래그로 방향 조정 가능)  
`Q / E + 우클릭` : Secen View의 화면 보는 방향 기준 높이를 변경한다. (우클릭 드래그로 방향 조정 가능)  
`Ctrl + Alt + 좌클릭` : 보는 방향에 수평인 평면의 상/하/좌/우로 움직인다.  

 - Game View :  
 **Scene View**와 동일한 위치에 디폴트되는 창으로 **Scene View**에 시각화한 오브젝트와 만든 코드, 애니메이션 등의 동작을 확인하는 시뮬레이터라고 생각하면 될 것 같다.  
 <br>상단의 플레이 버튼으로 **Game View**를 활성화 시킬 수 있으며, **Scene View**에서 사용중인 오브젝트, 오브젝트에 포함된 컴포넌트 등 사용할 수 없는 항목이 있으면 실행이 되지 않고 에러를 뱉는다.  
 에러는 **Console** 창에서 볼 수 있으며, Unity Editor(프로그램)화면에서 **Console**창이 안보인다면 상단 도구에서 [Window] - [General] - [Console] 버튼을 클릭하면 볼 수 있다.  
 <br>**Game View**에서는 화면의 이동은 자유롭게 이뤄지지 않으며, Camera 오브젝트가 보는 화면만을 볼 수 있다.  
 즉, 코드를 사용해 Camera를 이동시키면 된다. 만든 코드로 작동하는 동작들, 이벤트들을 시험해 볼 수 있으며, 외부 DB나 Server와의 연결도 시험해 볼 수 있다.  

### Inspector View
이미지의 3번에 해당하는 **Inspector View**는 선택한 오브젝트의 정보를 보여주는 창이다.  
**Hierarchy** 또는 **Scene**에서 선택한 오브젝트의 **Transform**, **Tag**, **Name** 포함된 **Componenet**등 해당 오브젝트의 세세한 정보들을 확인하고, 수정할 수 있다.  
이름 좌측에는 체크박스가 존재 하는데 **Scene View**에서 해당 오브젝트를 보여줄 것인지 체크해주는 박스다. 해당 기능은 **Unity Monobehavior**의 기본 메서드 중 **OnEnable**, **OnDisable** 메서드를 동작하게 하는 트리거가 된다.  
코드에서 해당 오브젝트의 정보를 접근할 때도 **Inspector View**에서 보는 정보들은 모두 접근이 가능하다. 반대로, 코드에서 선언한 변수를 **Public**형식으로 선언하는 경우 **Inspector View**에서 접근이 가능하다.  
<br>**Game View**를 통해 프로젝트를 테스트하는 경우 코드를 수정하면 에러가 나오면서 동작하지 않지만, **Inspector View**에서 값을 수정하면 에러가 나오지 않아 실시간으로 수정하며 기능을 테스트 할 수 있다. **단, 플레이를 끝낸 후에는 수정한 사항들이 전부 초기화 되므로 주의 해야 한다.**

### Project View
이미지의 4번에 해당하는 **Project View**는 해당 프로젝트의 디렉토리를 볼 수 있는 창이다.  
포함된 **Resource**, **Sound**, **Prefab**, **Script** 등을 관리 할 수 있으며, 일부 파일의 경우 Drag & Drop으로 **Hierarchy**, **Scene**에 포함이 가능하다.  
해당 프로젝트의 **Assets** 디렉토리의 하위 디렉토리 및 파일만 볼 수 있으므로 상위 디렉토리 또는 형제 디렉토리의 경우 컴퓨터의 해당 프로젝트 위치로 가서 확인해야 한다.  

## Unity 구성화면 변경하기
앞서 기술한 사항들은 Unity의 Default 구성 화면이다. 하지만, 사용자에 따라 원하는 View의 종류나 위치를 변경할 수 있도록 Unity는 배려해줬다.  
우선 파일집의 네임택 같은 부분을 !["Name_Tag.png"](/assets/img/2022-08-24-Unity-View/NameTag.png "View Name Tag")   
Drag & Drop으로 옮길 수 있다. 옮길 수 있는 위치가 꽤나 다양하고 상단 도구 중 [Window] 에서 필요한 View들을 선택해 마구 추가해도 무관하다.  
열심히 공들여 변경한 구성화면을 다른 프로젝트에서도 사용하고 싶다면 상단 도구 중 [Window] - [Layouts] - [Save Layout...] 을 사용해 현재 구성화면을 저장하도록 하자.  
!["My_Layout.png"](/assets/img/2022-08-24-Unity-View/My_Layout.png "My Layout")   
현재 세개정도의 나만의 Layout을 만들어 사용중에 있다. 작업마다 필요한 도구나, 배치가 달라 자주 작업하는 Layout을 만들어 놓고 사용하면 편리하다.  
<br>현재 프로젝트를 작업하는 경우에는 해당 **Layout**을 사용한다.
!["Change_Layout.png"](/assets/img/2022-08-24-Unity-View/Change_Layout.png "Change Layout")   
Layout을 저장할 때 보였겠지만 Unity에서 제공하는 Layout이 여러가지가 있다. 처음에 감이 잡히지 않는 다면 해당 Layout을 사용하면서 점차 자신만의 Layout을 만들면 될 것 같다.