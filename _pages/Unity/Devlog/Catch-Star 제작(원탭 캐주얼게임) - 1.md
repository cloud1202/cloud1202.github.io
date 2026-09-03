---
title: "Catch-Star 제작(원탭 캐주얼게임) - 1"
date: 2026-09-04
categories: [Unity, Devlog]
tags: [Catch-Star, 개발일지, Devlog, Unity, Unity2D, C#, 원탭게임]
description: "원탭 캐주얼 게임 Catch-Star를 만들기 시작했습니다. 첫날은 위성 공전·자전 프로토타입. 공전은 cos/sin으로 좌표를 직접 찍고 자전은 위성이 각자 돌게 나눴습니다. 하드코딩으로 남겨둔 부분까지 그대로 기록합니다."
author: OC
is_post: true
thumbnail: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 1/thumbnail.png"
imgAddress: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 1/"
---

## 오늘 한 것: 위성 공전·자전 프로토타입

원탭 캐주얼 게임을 하나 개인 프로젝트로 시작했습니다. 이름은 `Catch-Star`. 완성될지 어떨지도 모르겠지만, 만드는 동안 뭘 했는지는 남겨두는 게 나중에 도움이 될 것 같아서(본인 기준) 이렇게 기록을 시작합니다. 잘 정리된 강의 같은 글이 아니라 그날 작업 일지에 가깝습니다.

거두절미하고 본론으로. 오늘은 **위성이 행성 주위를 도는 공전**과 **위성 자체가 제자리에서 도는 자전**을 붙였습니다. 프로젝트 골격을 처음 올린 날이라 이것저것 딸려 들어갔지만, 실제로 손으로 친 건 스크립트 두 개가 전부다.

![Unity 게임 뷰 실행 화면. 점선 궤도를 따라 위성이 공전하면서 스프라이트 자체도 함께 회전한다]({{page.imgAddress}}body-0.gif)

돌려보면 이렇게 나옵니다. 그런데 화면에 잡히는 위성은 3기 중 1기뿐입니다. 궤도 중심을 `(0, -3)`으로 박아둬서 나머지 둘은 카메라 밖에 있다.

---

## 공전은 cos/sin으로 좌표를 직접 찍었다

`Transform.RotateAround`나 빈 부모 오브젝트를 회전시키는 방법 대신 `Mathf.Cos`/`Mathf.Sin`으로 매 프레임 좌표를 새로 계산했습니다. 이유는 하나인데, **지금 몇 도째인지와 반경을 코드가 직접 들고 있는 편이 나중에 편할 것 같아서**입니다(본인 기준). 빈 부모 회전 방식은 부모 스케일이 균일하지 않으면 자식이 찌그러질 수 있다고 해서 일단 미뤄뒀다.

![cos/sin 직접 계산, Transform.RotateAround, 빈 부모 오브젝트 회전 세 방식의 코드 길이·각도 추적·부모 스케일 영향·대표 함정 비교 표]({{page.imgAddress}}body-1.png)

좌표를 찍는 부분은 이게 전부입니다.

```csharp
offset += addOffset;
float radian = offset * Mathf.Deg2Rad;

float x = Mathf.Cos(radian) * DISTANCE;
float y = Mathf.Sin(radian) * DISTANCE - 3f;
satellite.transform.position = new Vector3(x, y, 0f);
```

각도를 `offset`에 계속 더하고 `Mathf.Deg2Rad`로 라디안으로 바꿔서 좌표를 찍습니다. 배치는 시작 각도를 한 번만 뽑고 거기에 120도씩 더하는 식이다.

```csharp
float offset = Random.Range(0f, 360f);
for (int i = 0; i < 3; i++)
{
    m_data[i].satellite = SpawnSatellite();
    m_data[i].offset = (offset + i * 120f);
}
```

그래서 실행할 때마다 시작 방향은 다른데 간격은 항상 같습니다.

![중심 (0, -3), 반지름 3.6인 원 위에 위성 3기가 120도 간격으로 놓인 궤도 배치 다이어그램. 시작 각도 offset은 매 실행마다 랜덤이다]({{page.imgAddress}}body-2.png)

---

## 자전은 위성이 각자 돈다

자전은 링이 아니라 위성 본인(`Satellite.cs`)이 맡습니다. 링은 **위치**만 계산하고 위성은 **자기 z축 회전**만 담당하는 식으로 나눴습니다. 둘 다 초당 10도로 값은 같지만 인스펙터에서 따로 조절할 수 있어서 이렇게 두는 게 편했다.

```csharp
this.transform.localEulerAngles = new Vector3(0,0, m_angle);

m_angle += Time.deltaTime * m_speed;

if (m_angle > 360f) m_angle %= 360f;
```

스프라이트는 `Satellite_0`~`Satellite_6` 7종 중 하나를 아틀라스에서 랜덤으로 뽑아 씌웁니다. `SpriteAtlas.GetSprite`는 부를 때마다 스프라이트를 새로 복제해서 돌려주기 때문에 매 프레임 호출하면 안 되는데, 지금은 `Start`에서 한 번만 부르고 있어서 괜찮습니다.

---

## 다음에 할 것

지금은 값을 코드에 박아둔 상태라, 하드코딩한 것들부터 인스펙터로 빼고 궤도 중심을 행성 트랜스폼 기준으로 잡을 생각입니다. 그다음이 게임다운 부분(별을 잡는 조작)이 될 것 같다.

---

*참고 소스*

- [Mathf.Deg2Rad - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/Mathf.Deg2Rad.html)
- [Transform.RotateAround - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/Transform.RotateAround.html)
- [SpriteAtlas.GetSprite - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/U2D.SpriteAtlas.GetSprite.html)

<!--
게시 전 체크 (naver-seo-guide.md / google-guide.md 반영 메모, 발행 시 삭제 가능)

[제목] "Catch-Star 제작(원탭 캐주얼게임) - 1" — 공백 포함 27자. 시리즈 1편 고정 형식.
  google-guide 50~60자 이내 충족. naver 15~25자 권장을 1자 초과하나 시리즈 넘버링 형식이라 유지.
  메인 키워드 "Catch-Star"가 맨 앞. 특수문자는 하이픈·괄호만, 낚시성 문구 없음.

[본문 분량] 공백 제외 1,003자 (코드 블록·이미지 태그·링크·프론트매터·이 주석 제외한 순수 본문).
  코드 블록 포함 시 공백 제외 2,029자.
  저자 요청 반영 이력:
   - 커밋 통계(파일 수·삽입 줄 수·스크립트 줄 수) 언급 전부 삭제
   - 코드는 전문 대신 필요한 부분만 발췌 (6줄 / 6줄 / 5줄 3블록). 발췌한 줄은 실제 소스 원문 그대로
   - "아직 안 된 것들" 미완성 목록 절 삭제, "다음에 할 것" 두 줄로 대체
  이전 상세 원고(draft-detailed-backup.md, 코드 포함 공백 제외 12,815자) 대비 약 79% 축약.
  기록 일지 성격이라 의도적으로 짧게 유지 — naver 권장 1,500~2,000자에는 못 미치므로,
  시리즈가 쌓이면 C-Rank는 편수와 주제 집중도로 확보하는 방향.

[키워드 배치] 핵심 키워드: "Catch-Star", "원탭 캐주얼게임", "Unity 개발일지", "위성 공전 자전", "cos/sin"
  - 제목: Catch-Star, 원탭 캐주얼게임
  - 도입부: Catch-Star, 공전, 자전
  - 소제목: 공전 cos/sin, 자전
  - 마무리: 궤도 중심, 다음 작업
  기계적 반복 없이 문맥상 자연스러운 빈도로 분산.

[이미지] 총 3장 사용 + 썸네일 1장, 전부 원본 (D.I.A+ 원본성 대응). 제작 완료 상태 재사용.
  body-0.gif  게임 뷰 실행 녹화 — 저자 직접 캡처
  body-1.png  공전 3방식 비교 표
  body-2.png  궤도 배치 다이어그램 (반지름 3.6 / 중심 (0,-3) / 120도 간격 3기)
  thumbnail.png  1080x1080 대표 이미지
  미사용(파일은 보존): body-3.png(공전·자전 설정값 비교 표), body-4.png(Update 구조 비교)
  주의: body-0만 확장자가 .gif다. Publisher의 이미지 태그 치환 시 .png로 가정하지 말 것.
  alt 텍스트는 전부 125자 이내로 작성 완료.

[네이버 해시태그] #Unity #유니티개발일지 #CatchStar #게임개발

[구글] description 공백 포함 125자 — 권장 120~158자 범위 충족.
  JSON-LD는 Jekyll SEO tag가 front matter(title/date/author/description) 기반으로 자동 생성됨.

[애드센스] 광고 삽입 권장 위치 — 첫 문단 앞 배치 금지. 글이 짧으므로 2개 이하 권장.
  1) "공전은 cos/sin으로..." 섹션 시작 직전 (도입부 이후)
  2) 본문 종료 후(참고 소스 아래)
  각 슬롯에 고정 height 지정해 CLS 방지.
-->
