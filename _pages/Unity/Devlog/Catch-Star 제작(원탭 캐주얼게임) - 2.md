---
title: "Catch-Star 제작(원탭 캐주얼게임) - 2"
date: 2026-09-08
categories: [Unity, Devlog]
tags: [Catch-Star, 개발일지, Devlog, Unity, Unity2D, C#, 원탭게임]
description: "Catch-Star 두 번째 개발일지입니다. 타이머에 따라 줄어드는 고리, 콤보에 물린 각속도, 상단 90도 기준 판정창까지 붙였습니다. 각도 누적을 버리면서 1편의 360도 문제가 사라진 이야기도 함께 적었습니다."
author: OC
is_post: true
thumbnail: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 2/thumbnail.png"
imgAddress: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 2/"
---

## 오늘 한 것: 줄어드는 고리와 별을 잡는 조작

1편 마지막에 "하드코딩한 것들부터 인스펙터로 빼고, 그다음이 게임다운 부분"이라고 적어뒀는데 오늘 그게 다 됐습니다. 타이머에 맞춰 고리가 줄어들고, 터치하면 판정이 들어가고, 콤보가 쌓이면 위성이 빨라집니다. 게임 루프라 부를 만한 게 이제야 하나 생겼다.

위성별 데이터(`id`, `comboRange`, `value`)는 **ScriptableObject로 뺐습니다.** 인스턴스마다 복사본을 갖는 대신 자산 하나를 참조로 공유하는 게 이 클래스의 원래 용도라고 하니 맞게 쓴 것 같습니다. 다만 struct를 SO로 옮기는 순간 기존 `SatelliteRing.cs` 안의 같은 이름과 겹쳐 `CS0101`이 났다. 링 쪽을 `SatelliteObject`로 개명해 넘어갔다.

---

## 각도를 더하지 않으니 360도 문제가 사라졌다

결론부터 말하면 **회전 방식을 바꿨더니 1편에서 빠뜨렸던 버그가 알아서 없어졌습니다.** 1편에서는 `offset += Time.deltaTime * speed`로 각도를 계속 더했고, 값이 무한정 커지는데 wrap 처리를 안 해뒀다. 지금은 타이머 경과 비율에서 매번 새로 계산합니다.

```csharp
m_timer += Time.deltaTime;
var velocity = m_timer / m_duration;
m_currentOffset = 360f * velocity;
m_currentRadius = Mathf.Lerp(BASE_RADIUS, BASE_RADIUS * 0.5f, velocity);
transform.localScale = Vector3.one * m_baseScale * (m_currentRadius / BASE_RADIUS);
```

비율 하나로 각도와 반지름을 동시에 굴립니다. 각도는 `360f * velocity`라 한 바퀴를 넘길 일이 없고, 반지름은 3.6에서 1.8까지 줄어듭니다. `Mathf.Lerp`는 `t`가 0~1로 자동 클램프되니 경과 비율을 그대로 넣어도 안전합니다.

`localScale`까지 건드린 이유는 씬에 그려둔 고리 스프라이트 때문이다. 반지름만 줄이면 위성은 안으로 들어오는데 그림은 그대로라 둘이 따로 논다. 그래서 반지름 비율을 스케일에도 먹였습니다. 최선은 아닌 것 같아(본인 기준) TODO로 남겨뒀다.

![타이머가 진행되면서 고리 반지름이 3.6에서 1.8로 줄어드는 과정. t=0, 0.5, 1.0 세 시점의 원 크기와 위성 위치 비교]({{page.imgAddress}}body-1.png)

---

## 콤보가 오르면 한 바퀴가 빨라진다

```csharp
private float[] m_angularVelocity = new float[4] { 100, 140, 180, 240 };

m_duration = 360f / m_angularVelocity[m_comboIndex];
```

콤보 구간이 각속도를 고르고, 각속도가 한 바퀴 시간을 정합니다. 콤보 10 미만이면 초당 100도라 한 바퀴에 3.6초, 30을 넘기면 초당 240도라 1.5초. 처음엔 속도를 상수로 박아뒀는데 돌려보니 너무 빨라서 배열로 빼고 콤보에 물렸습니다. 난이도 곡선을 숫자 네 개로 만지면 되니 이쪽이 나았다.

![콤보 구간별 각속도와 한 바퀴 시간 비교 표. 콤보 0~9는 초당 100도 3.6초, 10~19는 140도, 20~29는 180도, 30 이상은 240도 1.5초]({{page.imgAddress}}body-2.png)

---

## 판정은 상단 90도에서 좌우 60도씩

```csharp
var deltaAngle = Mathf.DeltaAngle(m_satellites[i].offset, 90f);
if (deltaAngle <= 60f && -60f < deltaAngle)
```

처음엔 위성 위치 벡터와 위쪽 단위 벡터로 각도를 구할까 고민했는데, 어차피 좌표를 각도에서 만들어 쓰는 중이라 각도를 좌표로 바꿨다가 되돌릴 이유가 없었다. `Mathf.DeltaAngle`은 두 각도의 최단 차이를 -180~180 범위로 돌려주니 350도와 10도처럼 경계를 넘는 경우도 뺄셈처럼 어긋나지 않습니다.

판정창은 기획 단계에서 115도로 잡았다가 120도로 확정했습니다. 5도 차이가 대수인가 싶지만 한 바퀴가 1.5초까지 빨라지는 구간에서는 이 폭이 곧 체감 난이도다.

![캐치 판정창 다이어그램. 원 위쪽 90도를 중심으로 좌우 60도씩 총 120도 구간이 판정 영역으로 강조된 그림]({{page.imgAddress}}body-3.png)

---

## 다음에 할 것

콤보가 끊기는 조건을 아직 안 만들어서 지금은 쌓이기만 합니다. 여기부터 손볼 생각입니다.
그다음은 잡았을 때와 놓쳤을 때의 연출이 될 것 같다.

---

*참고 소스*

- [Mathf.DeltaAngle - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/Mathf.DeltaAngle.html)
- [Mathf.Lerp - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/Mathf.Lerp.html)
- [ScriptableObject - Unity 공식 매뉴얼](https://docs.unity3d.com/Manual/class-ScriptableObject.html)

<!--
게시 전 체크 (naver-seo-guide.md / google-guide.md 반영 메모, 발행 시 삭제 가능)

[제목] "Catch-Star 제작(원탭 캐주얼게임) - 2" — 공백 포함 27자. 1편과 동일한 시리즈 고정 형식.
  google-guide 50~60자 이내 충족. naver 15~25자 권장을 1자 초과하나 시리즈 넘버링 형식이라 유지.
  메인 키워드 "Catch-Star"가 맨 앞. 특수문자는 하이픈·괄호만, 낚시성 문구 없음.

[본문 분량] 공백 제외 1,063자 (소제목 제외 순수 본문 / 소제목 포함 시 1,146자).
  코드 블록·이미지 마커·참고 링크·프론트매터·이 주석은 제외한 수치. 1편(902자)과 같은 1,000자 내외 분량대.
  저자 요청 반영 사항:
   - 커밋 통계(파일 수·줄 수·스크립트 줄 수) 일절 미언급
   - 코드는 전문 대신 본문이 실제로 설명하는 부분만 발췌 (5줄 / 3줄 / 2줄, 총 3블록)
   - 발췌한 줄은 실제 소스 원문 그대로. 가독성 목적의 리라이팅 없음
   - "아직 안 된 것들" 미완성 목록 절 없음, "다음에 할 것" 두 줄로 대체
   - research.md 근거는 Lerp 클램프 / DeltaAngle 반환 범위 / SO 데이터 공유 세 군데에만 한 문장씩
  기록 일지 성격이라 의도적으로 짧게 유지 — naver 권장 1,500~2,000자에는 못 미치므로,
  C-Rank는 시리즈 편수와 주제 집중도로 확보하는 방향.

[키워드 배치] 핵심 키워드: "Catch-Star", "원탭 캐주얼게임", "Unity 개발일지", "콤보 각속도", "Mathf.DeltaAngle"
  - 제목: Catch-Star, 원탭 캐주얼게임
  - 도입부: Catch-Star(제목 연계), 타이머, 콤보, 게임 루프
  - 소제목: 360도/각도, 콤보·각속도, 판정 90도·60도
  - 마무리: 콤보 초기화, 연출
  기계적 반복 없이 문맥상 자연스러운 빈도로 분산.

[이미지] [IMAGE: ...] 마커 3개. 전부 HTML+CSS로 제작 가능한 다이어그램·표이며 실제 촬영 불필요.
  1) 고리 반지름 3.6 → 1.8 축소 다이어그램
  2) 콤보 구간별 각속도·한 바퀴 시간 비교 표
  3) 캐치 판정창 다이어그램 (상단 90도 기준 좌우 60도, 총 120도)
  별도로 [FOOTAGE-TODO: ...] 한 줄은 저자가 직접 녹화해 채울 플레이 영상 자리다.
  image-maker는 이 줄을 건드리지 않는다.
  썸네일 1080x1080 별도 제작 필요.
  alt 텍스트는 마커 설명을 125자 이내로 다듬어 최종 삽입할 것.

[네이버 해시태그] #Unity #유니티개발일지 #CatchStar #게임개발

[구글] description 공백 포함 120자 — 권장 120~158자 범위 충족.
  JSON-LD는 Jekyll SEO tag가 front matter(title/date/author/description) 기반으로 자동 생성됨.

[애드센스] 광고 삽입 권장 위치 — 첫 문단 앞 배치 금지. 글이 짧으므로 2개 이하 권장.
  1) "각도를 더하지 않으니..." 섹션 시작 직전 (도입부 이후)
  2) 본문 종료 후(참고 소스 아래)
  각 슬롯에 고정 height 지정해 CLS 방지.
-->
