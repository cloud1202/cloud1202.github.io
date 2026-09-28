---
title: "Catch-Star 제작(원탭 캐주얼게임) - 4"
date: 2026-09-29
categories: [Unity, Devlog]
tags: [Catch-Star, 개발일지, Devlog, Unity, Unity2D, C#, 원탭게임, 리듬게임, PlayScheduled, dspTime]
description: "Catch-Star 네 번째 개발일지입니다. 8번 탭하면 끝나던 사운드 프로토를 인공위성·게이지가 있는 원탭 리듬게임 방식으로 바꿨습니다. 거리 기반 옥타브 판정과, 노트가 늘자 곡이 씹혀 0.5초씩 굴려 예약하게 된 이야기를 적었습니다."
author: OC
is_post: true
thumbnail: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 4/thumbnail.png"
imgAddress: "/assets/img/Catch-Star 제작(원탭 캐주얼게임) - 4/"
---

## 오늘 한 것: 8번 탭하면 끝나던 판을 리듬게임으로

3편 마지막에 스폰 템포와 판이 끝나는 조건부터 다시 보겠다고 적었다. 위쪽에 위성이 모여 화음이 되는 순간은 좋은데 랜덤이라 붕 뜨는 시간이 많고, **8번 탭하면 끝나는 건 게임보다는 사운드 테스트**에 가까웠다(본인 기준).

그래서 **원탭 리듬게임 방식**으로 틀었습니다. 스폰 간격은 `Random.Range(0.35f, 0.5f)`초로 확 줄였고, 판이 끝나는 조건은 두 가지다. 회색 **인공위성**을 다시 만들어 이걸 잡으면 끝. 상단 **게이지**는 기본 15초로 시간이 지나면 줄고 잡으면 조금 차는데, 0이 돼도 끝이다. 빈 공간 탭은 그대로 쉼표. 2편부터 끌고 온 콤보 시스템은 아예 지우고, 결과 화면에서 캐치 개수와 곡 길이를 보여주기로 했습니다.

![Catch-Star 플레이 GIF. 7색 음표 위성과 회색 인공위성이 위쪽 호를 따라 지나가고, 상단 캐치존에서 탭해 잡는 장면]({{page.imgAddress}}gameplay.gif)

소리 쪽도 바뀌었다. 3편은 샘플 하나를 `pitch`로 늘려 7음을 냈는데, 이번엔 CC0 라이선스라 상업적으로 써도 되는 **VCSL**에서 악기별로 골라 위성 데이터(SO)에 옥타브별 `AudioClip` 세 개를 넣었다. 실제 샘플이 있으니 피치 변환은 사라졌습니다.

```csharp
// 옥타브별 실제 샘플이 SO에 들어 있으므로 피치 변환 없음
var clip = _bank.GetClip(n.degrees[v], oct);
```

---

## 판정 결과가 점수가 아니라 옥타브라면?

3편은 각도로 봤다. 캐치존 안에서 90도를 아직 안 지난 리딩 밴드면 한 옥타브 위였다. 이번엔 위성보다 20% 정도 큰 캐치존과 위성 중심 사이의 **거리**로 봅니다.

```csharp
var dis = Vector2.Distance(obj.satellite.transform.position, m_catchZone.transform.position);
float radius = obj.satellite.spriteRenderer.bounds.extents.x;
...
int octave = dis <= radius * 0.15 ? 1 : dis <= radius * 0.5 ? 0 : -1;
```

반지름의 15% 이내면 High, 50% 이내면 Mid, 그 밖이면 Low. 85%보다 멀면 못 잡은 걸로 친다. 기획 때 Perfect/Bad 같은 잘했다·못했다 표현은 쓰지 말자고 정했는데, 정확도가 **음높이**로 들어가니 그 의도가 코드에 그대로 옮겨진 것 같다(본인 기준). 대신 캐치존이 하나라 한 번에 한 음만 잡혀서, 3편에서 좋았던 화음은 오히려 안 나온다.

![거리 기반 옥타브 판정 다이어그램. 위성 중심에서 반지름 15% 이내 High(+1옥타브), 50% 이내 Mid(기준), 85% 이내 Low(-1옥타브), 그 밖은 캐치 실패로 나뉜 동심원]({{page.imgAddress}}body-1.png)

---

## 곡을 틀었더니 노트가 씹혔다

박자 기록도 바꿨다. 3편은 `slot`에 탭 순서를 넣고 0.3초 간격으로 줄 세웠는데, 이번엔 첫 캐치부터 돈 녹음 시계 값을 노트의 `time`에 그대로 넣는다.

```csharp
public float  time;      // 게임 시작 기준 초 (float). 양자화 없음
```

슬롯 기반으로 짜놓은 걸 실시간 기반으로 바꾸려니 이게 꽤 헷갈렸다.

진짜 문제는 재생이었다. 3편은 곡이 8노트라 한 번에 예약해도 AudioSource 24개 풀로 충분했는데, 노트가 늘자 **곡 전체가 안 나오고 중간중간 씹혔습니다.** 원인은 곡 전체를 한 프레임에 예약한 것. AudioSource 하나는 예약을 하나만 들고 있는 것처럼 동작해서, 보이스를 재사용하는 순간 아직 안 울린 앞 노트의 예약이 날아갔다. 공식 문서에 적혀 있진 않지만 Unity 포럼에서도 같은 현상이 보고돼 있다. 그래서 **0.5초 앞까지만 굴려가며** 예약하도록 바꿨습니다.

```csharp
while (idx < notes.Count &&
       baseT + notes[idx].time <= AudioSettings.dspTime + ScheduleAhead)
{
    tail = Math.Max(tail, ScheduleNote(notes[idx], baseT + notes[idx].time));
    idx++;
}
```

빈 보이스가 없으면 가장 먼저 끝나는 걸 뺏어 쓴다. 포럼 답변에 나온 방식(가까운 미래만 예약 + 보이스 뺏기)과 같은 구조다. 예약 시각은 3편처럼 `dspTime` 위의 절대 시각이라, 녹음한 `time`에 재생 시작 시각 `baseT`만 더하면 된다.

![0.5초 앞까지만 굴려 예약하는 타임라인 다이어그램. dspTime 현재 시각부터 0.5초 창 안에 든 노트만 예약되고, 창이 앞으로 밀리며 다음 노트가 들어오는 모습]({{page.imgAddress}}body-2.png)

게임오버 패널의 재생 버튼을 누르면 곡이 나온다.

![Catch-Star 게임오버 패널. 상단 재생 버튼, 곡 길이 20.2초, 색깔별 위성 캐치 개수, 하단 공유·홈·재시도 버튼]({{page.imgAddress}}screen-2.png)

---

## 다음에 할 것

캐치존을 공전 고리 전체로 넓히고, 위성이 위에서 떨어지는 노트 리듬게임 방식으로 바꿔볼 생각입니다. 화음이 나오게 하려는 게 목적이다.
게이지바는 빼고, 놓친 위성이 행성에 부딪혀 행성이 부서지는 연출로 대신해볼 것 같다.

---

*참고 소스*

- [AudioSource.PlayScheduled - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html)
- [AudioSettings.dspTime - Unity 공식 Scripting API](https://docs.unity3d.com/ScriptReference/AudioSettings-dspTime.html)
- [call AudioSource.PlayScheduled() x times without cancelling original call - Unity Discussions](https://discussions.unity.com/t/call-audiosource-playscheduled-x-times-without-cancelling-original-call-procedural-audio-question/685804)
- [sgossner/VCSL - GitHub](https://github.com/sgossner/VCSL)

<!--
게시 전 체크 (naver-seo-guide.md / google-guide.md 반영 메모, 발행 시 삭제 가능)

[제목] "Catch-Star 제작(원탭 캐주얼게임) - 4" — 공백 포함 27자. 1~3편과 동일한 시리즈 고정 형식(부제 없음).
  google-guide 50~60자 이내 충족. naver 15~25자 권장을 약간 초과하나 시리즈 넘버링 형식이라 유지.
  메인 키워드 "Catch-Star"가 맨 앞. 특수문자는 하이픈·괄호만, 낚시성 문구 없음.

[본문 분량] 공백 제외 1,188자 (소제목·코드·이미지·참고 링크·프론트매터·이 주석 제외 순수 본문).
  저자 요청 반영 사항:
   - 편 삽입으로 기존 3편 원고를 4편으로 재구성. 도입부는 새 3편의 "다음에 할 것"(스폰 템포·판 종료 조건 / 붕 뜨는 시간)을 이어받음
   - 방향 전환은 "8번 탭하면 끝나는 사운드 프로토 → 원탭 리듬게임 방식(인공위성·게이지·쉼표 유지·콤보 제거)"으로 서술. "위성이 음이 되고 곡으로 재생"은 3편에서 이미 한 이야기라 새로 소개하지 않음
   - 3편 연결점: pitch 변환 → 옥타브별 실제 샘플 / slot(탭 순서) → 실시간(초)·양자화 없음 / 8노트 일괄 예약 → 0.5초 굴려 예약 / 각도(리딩 밴드) → 거리 High/Mid/Low
   - dspTime·PlayScheduled 기본 설명은 3편에서 했으므로 한 문장으로 축소
   - 커밋 통계 미언급, 코드는 원문 그대로 짧게 발췌 (2줄 / 4줄 / 1줄 / 6줄, 총 4블록)
   - 한계(캐치존 하나라 화음 불가)는 본문 한 문장으로 처리
  naver 권장 1,500~2,000자에는 못 미치나 시리즈 기록 일지 성격이라 의도적으로 짧게 유지.

[키워드 배치] 핵심 키워드: "Catch-Star", "원탭 캐주얼게임", "리듬게임", "옥타브 판정", "PlayScheduled", "dspTime"
  - 제목: Catch-Star, 원탭 캐주얼게임
  - 도입부: 원탭 리듬게임, 인공위성, 게이지, VCSL
  - 소제목: 리듬게임, 옥타브, 노트 씹힘
  - 본문: PlayScheduled(코드), dspTime, 보이스 풀
  기계적 반복 없이 분산.

[이미지] 실제 캡처·도식 4장 (모두 images/에 있음, 새 [IMAGE:] 마커 없음).
  1) ./images/gameplay.gif — 도입부 플레이 GIF
  2) ./images/body-1.png — 거리 기반 옥타브 판정 동심원 다이어그램 (15% / 50% / 85%)
  3) ./images/body-2.png — 0.5초 앞까지만 굴려 예약하는 타임라인 다이어그램
  4) ./images/screen-2.png — 게임오버 패널
  썸네일 1080x1080 별도 제작 필요.
  캡처 이미지 경로는 발행 시 사이트 imgAddress 관례({{page.imgAddress}})로 바꿀지 확인.

[네이버 해시태그] #Unity #유니티개발일지 #CatchStar #게임개발

[구글] description 공백 포함 133자 — 120~158자 범위 확인.
  JSON-LD는 Jekyll SEO tag가 front matter(title/date/author/description) 기반으로 자동 생성됨.

[애드센스] 첫 문단 앞 배치 금지. 글이 짧으므로 2개 이하 권장.
  1) "판정 결과가 점수가 아니라 옥타브라면?" 섹션 시작 직전
  2) 본문 종료 후(참고 소스 아래)
  각 슬롯에 고정 height 지정해 CLS 방지.
-->
