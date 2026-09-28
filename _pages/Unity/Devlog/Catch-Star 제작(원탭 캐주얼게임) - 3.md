---
title: "Catch-Star 제작(원탭 캐주얼게임) - 3"
date: 2026-09-12
categories: [Unity, Devlog]
tags: [Catch-Star, 개발일지, Devlog, Unity, Unity2D, C#, 원탭게임, struct, AudioSource, PlayScheduled]
description: "Catch-Star 세 번째 개발일지입니다. 7음계를 위성으로 만들고 8번 탭하면 모은 음을 곡으로 들려주는 첫 사운드 프로토타입을 붙였습니다. struct를 List에 넣었다가 위성이 제자리걸음한 이야기도 적었습니다."
author: OC
is_post: true
thumbnail: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 3/thumbnail.png"
imgAddress: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 3/"
---

## 오늘 한 것: 점수 게임에 소리를 붙였다

2편 마지막에 "콤보가 끊기는 조건, 그다음은 연출"이라고 적어뒀는데 둘 다 손을 못 댔다. 대신 소리 쪽으로 먼저 방향이 잡혔습니다. **도~시 7음계를 전부 위성으로** 만들었다. 범위 시작 지점에서 랜덤 간격으로 나오고, **8번 탭하면 모은 음을 곡으로 들려줍니다.**

![Catch-Star 사운드 프로토타입 플레이 GIF. 검은 배경에서 도~시 7색 파스텔 마름모 위성이 흰 행성 위 점선 궤도를 따라 도는 장면]({{page.imgAddress}}gameplay.gif)

---

## 위성이 왜 제자리걸음을 했을까?

결론부터 말하면 **struct를 `List`에 넣고 인덱서로 메서드를 불렀기 때문**이었다. 공전시키려고 돌렸는데 위성이 전부 제자리에 서 있었다.

```csharp
public struct SatelliteObject
...
        offset += addOffset;
...
m_rotateSatellites[i].RotationSatellite(Time.deltaTime * m_speed, BASE_RADIUS);
```

`List<T>`의 인덱서는 저장 공간이 아니라 get 접근자, 즉 메서드라서 T가 struct면 **복사본**을 돌려줍니다. 필드에 바로 대입했으면 CS1612 에러라도 났을 텐데, 메서드 호출은 C# 사양상 임시 변수를 만들어 거기에 호출하니 에러 없이 넘어간다. `offset += addOffset`은 버려지는 복사본에만 들어가고 원본은 매 프레임 그대로였던 것.

해결은 `struct`를 `class`로 바꾼 한 단어. CS1612 문서에 적힌 해결책이기도 하다. 2편에서 이름이 겹쳐 개명했던 그 struct가 이번엔 발목을 잡았다.

![List 인덱서가 struct 복사본을 돌려주는 과정 도식. 리스트 안 원본(offset 10)과 인덱서가 만든 복사본을 나란히 두고, RotationSatellite가 복사본의 offset만 올린 뒤 복사본이 버려지고 원본은 10 그대로인 흐름. 옆에 class로 바꾸면 인덱서가 참조를 돌려줘 원본이 바뀌는 비교]({{page.imgAddress}}body-1.png)

---

## 탭 한 번이 노트 하나

```csharp
var deltaAngle = Mathf.DeltaAngle(obj.offset, CATCH_ZONE_CENTER);
if (deltaAngle > CATCH_ZONE_HALF || deltaAngle <= -CATCH_ZONE_HALF) continue;   // 존 밖

int degree = obj.satellite.Data.id;
int octave = deltaAngle > 0 ? 1 : 0;    // 리딩 밴드 = +1 옥타브
```

캐치존은 2편 그대로 상단 90도에서 좌우 60도. 탭하는 순간 존 안에 있는 위성 전부가 **한 노트(화음)**가 되고, 90도를 아직 안 지난 쪽은 한 옥타브 위로 친다. 같은 음이 양쪽에 동시에 걸리면 하나로 접고 높은 옥타브를 택한다. 빈 탭은 쉼표.

박자는 단순하게 갔습니다. `slot`에 **탭 순서**를 그대로 넣고, 실제 탭 간격은 버린 채 8분음표(BPM 100 기준 0.3초) 간격으로 줄 세운다.

아쉬운 건 존에 위성이 잘 안 모인다는 점. 스폰 간격이 `Random.Range(1, 8)`인데 int 오버로드라 1~7초 정수만 나오고, 화면에 위성이 한두 개뿐인 시간이 길다.

![Catch-Star 프로토타입 정지 화면. 흰 행성 위 점선 궤도 양 끝에 위성 두 개만 떠 있고 나머지는 비어 있는 모습]({{page.imgAddress}}screen-1.png)

---

## 샘플 하나로 7음을 내고, 절대 시각에 예약한다

```csharp
int midi = 60 + scale[Mathf.Clamp(n.degrees[v], 0, 6)] + 12 * oct + Transpose;
var z = sf.Nearest(midi);
float ratio = Mathf.Pow(2f, (midi - z.baseMidi) / 12f);
...
src.pitch  = ratio;
src.PlayScheduled(when);
```

음원 파일 이름에서 MIDI 번호를 파싱해 두고, 내야 할 음과 **가장 가까운 샘플**을 골라 반음 차이만큼 `pitch`를 조정한다. `pitch`는 재생 속도를 바꿔 생기는 음높이 변화고 평균율 반음은 주파수 비 2의 12제곱근이니, `2^(n/12)`면 n반음 이동이다. 속도가 바뀌는 만큼 멀리 늘릴수록 길이도 달라져서 가까운 샘플부터 고른다(본인 기준).

![가장 가까운 샘플에서 pitch를 올려 음을 내는 도식. 건반 위 C4 샘플에서 D4까지 2반음, pitch = 2^(2/12) 약 1.12, 반대로 한 반음 내리면 약 0.94. 샘플에서 멀어질수록 재생 속도 변화가 커진다는 화살표]({{page.imgAddress}}body-2.png)

재생에서 한 번 막혔다. **when이 뭐지?** `PlayScheduled`에 넘기는 값은 몇 초 뒤가 아니라 **dspTime 타임라인 위의 절대 시각**입니다. 지연 초를 넘기면 이미 지난 시각이라 전부 동시에 터진다. 그래서 `dspTime + 0.15`를 기준점으로 잡고 slot마다 0.3초씩 더한다. 0.15초는 공식 문서가 권하는 100~200ms 여유 안이고, 잡을 때 바로 울리는 피드백은 그러면 늦어서 0.02초로 따로 뒀다. 지금은 곡이 8노트라 한 번에 예약해도 AudioSource 24개 풀로 충분했다.

---

## 다음에 할 것

몇 판 돌려보니 속도가 느리고, 위성이 위쪽에 모여 화음이 되는 순간은 좋은데 랜덤이라 붕 뜨는 시간이 많다.
그래서 스폰 템포와 판이 끝나는 조건부터 다시 볼 생각입니다.

---

*참고 소스*

- [Compiler Error CS1612 - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/cs1612)
- [C# language specification - Expressions - Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/expressions)
- [Random.Range - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/Random.Range.html)
- [Audio Source component reference - Unity 공식 매뉴얼](https://docs.unity3d.com/Manual/AudioSource-reference.html)
- [Equal Temperament - SFU Sonic Studio Handbook](https://www.sfu.ca/sonic-studio-webdav/cmns/Handbook5/handbook/Equal_Temperament.html)
- [AudioSource.PlayScheduled - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html)
- [AudioSettings.dspTime - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/AudioSettings-dspTime.html)

<!--
게시 전 체크 (naver-seo-guide.md / google-guide.md 반영 메모, 발행 시 삭제 가능)

[제목] "Catch-Star 제작(원탭 캐주얼게임) - 3" — 공백 포함 27자. 1·2편과 동일한 시리즈 고정 형식(부제 없음).
  google-guide 50~60자 이내 충족. naver 15~25자 권장을 약간 초과하나 시리즈 넘버링 형식이라 유지.
  메인 키워드 "Catch-Star"가 맨 앞. 특수문자는 하이픈·괄호만, 낚시성 문구 없음.

[본문 분량] 공백 제외 1,148자 (소제목·코드·이미지·마커·참고 링크·프론트매터·이 주석 제외 순수 본문).
  저자 요청 반영 사항:
   - 커밋 통계 미언급
   - 코드는 본문이 설명하는 부분만 원문 그대로 발췌 (5줄 / 5줄 / 6줄, 총 3블록, 생략은 ...로 표시)
   - 미완성 목록 절 없음. 한계(스폰 정수 간격으로 빈 시간이 김)는 본문 한 문장으로 처리
   - research.md 근거는 CS1612·사양 임시 변수 / Random.Range int 오버로드 / pitch=재생 속도·2^(1/12) / PlayScheduled 절대 시각·100~200ms / dspTime double에 한두 문장씩
   - 4편 소재(실시간 기반 전환, 옥타브별 실제 샘플, 0.5초 굴려 예약, 노트 씹힘)는 미언급. "8노트라 한 번에 예약해도 충분했다" 한 문장만 복선으로 둠
  naver 권장 1,500~2,000자에는 못 미치나 시리즈 기록 일지 성격이라 의도적으로 짧게 유지.

[키워드 배치] 핵심 키워드: "Catch-Star", "원탭 캐주얼게임", "7음계 위성", "struct 복사본", "AudioSource pitch", "PlayScheduled", "dspTime"
  - 제목: Catch-Star, 원탭 캐주얼게임
  - 도입부: 7음계, 위성, 곡 재생
  - 소제목: 제자리걸음(struct), 탭·노트, 샘플·절대 시각
  - 본문: CS1612, pitch, PlayScheduled, dspTime
  기계적 반복 없이 분산.

[이미지] 실제 캡처 2장(이미 images/에 있음, 제작 불필요) + [IMAGE: ...] 도식 마커 2개(HTML+CSS 제작).
  1) ./images/gameplay.gif — 도입부 플레이 GIF
  2) [IMAGE] List 인덱서 struct 복사본 vs class 참조 도식
  3) ./images/screen-1.png — 위성 두 개만 뜬 빈 화면 (스폰 간격 한계 문장 옆)
  4) [IMAGE] 가장 가까운 샘플에서 pitch 2^(n/12) 적용 도식
  썸네일 1080x1080 별도 제작 필요.
  캡처 이미지 경로는 발행 시 사이트 imgAddress 관례({{page.imgAddress}})로 바꿀지 확인.

[네이버 해시태그] #Unity #유니티개발일지 #CatchStar #게임개발

[구글] description 공백 포함 122자 — 120~158자 범위 확인.
  JSON-LD는 Jekyll SEO tag가 front matter(title/date/author/description) 기반으로 자동 생성됨.

[애드센스] 첫 문단 앞 배치 금지. 글이 짧으므로 2개 이하 권장.
  1) "위성이 왜 제자리걸음을 했을까?" 섹션 시작 직전
  2) 본문 종료 후(참고 소스 아래)
  각 슬롯에 고정 height 지정해 CLS 방지.
-->
