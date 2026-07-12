---
title: "옵시디언 세컨드 브레인 만들기: PARA·MOC 플러그인 자동화"
date: 2026-07-12
categories: [Obsidian, Manual]
tags: [Obsidian, 옵시디언, Second Brain, 세컨드브레인, PARA, MOC, Templater, Zoottelkeeper, Folder Notes, 노트정리]
description: "옵시디언으로 세컨드 브레인을 구축하는 방법을 정리했다. PARA와 LYT·MOC 개념 비교부터 Folder Notes, Templater, Zoottelkeeper 조합으로 그래프뷰 전체를 자동 연결하는 실제 볼트 적용 후기까지 다룬다."
author: OC
---

## 옵시디언 세컨드 브레인 완전 분석

Tiago Forte는 자신의 책 *Building a Second Brain*(Atria Books, 2022)에서 아래와 같이 설명해주고 있다.

> "우리의 뇌는 아이디어를 저장하기 위한 것이 아니라, 아이디어를 갖기(having) 위한 것이다."

나는 이 말을 "머릿속에 다 담아두려 하지 말고, 디지털 공간에 외부 저장소를 만들어 거기서 아이디어를 꺼내 쓰라는 뜻"으로 이해하고 있습니다. Forte는 이 철학을 **CODE**라는 4단계 프레임워크로 구체화했는데, Capture(공감 가는 정보만 수집) → Organize(**PARA**로 실행 가능성 기준 정리) → Distill(점진적 요약) → Express(결과물로 표현) 순서입니다. 여기서 **PARA**(Projects·Areas·Resources·Archive)는 정보를 "주제"가 아니라 "지금 실행 가능한가"를 기준으로 나누는 조직화 방법론입니다.

옵시디언에서 세컨드 브레인을 이야기할 때 빠지지 않는 또 다른 축이 Nick Milo의 **LYT(Linking Your Thinking)**입니다. Milo는 2020년 옵시디언 초기 베타 테스터로 참여하면서 **MOC(Maps of Content)** 개념을 처음 소개했는데, 폴더로 가두는 대신 특정 주제를 "위에서 내려다보는" 허브 노트를 만들고 개별 노트는 링크로 자유롭게 연결시키는 방식입니다. 핵심 실행 프레임워크는 **ARC**(Add-Relate-Communicate)로, 아이디어를 모으고(Add) 관계를 만들고(Relate) 공유(Communicate)하는 3단계로 이뤄집니다.

![PARA 4단계(Projects·Areas·Resources·Archive)와 LYT MOC 허브 노트 개념을 비교한 다이어그램](./images/body-1.png)

### 왜 이 두 방법론을 알아야 하는가?

옵시디언을 처음 쓰기 시작하면 노트는 계속 늘어나는데 그래프뷰를 열어보면 서로 연결되지 않은 노드들이 점점이 흩어져 있는 상황을 마주치게 됩니다. 저도 처음엔 "일단 폴더부터 나누고 보자"는 마음으로 노트를 쌓았는데, 나중엔 어느 폴더에 뭘 넣었는지도 기억이 안 나고 그래프뷰는 그냥 흩어진 점들의 집합이더라구요.

**문제점 요약:** 폴더로만 분류하면 "분류는 됐지만 연결은 안 된" 상태가 되기 쉽고, 링크만 믿고 폴더를 안 쓰면 이번엔 "연결은 됐지만 어디서부터 봐야 할지 모르는" 상태가 됩니다.

**PARA·LYT/MOC의 역할:** PARA는 "이 노트를 지금 실행할 일인가, 계속 관리할 영역인가, 참고자료인가"를 기준으로 최소한의 폴더 뼈대를 잡아주고, LYT/MOC는 그 위에서 노트끼리 링크로 실제 연결망을 만들어줍니다. 즉 둘은 경쟁 관계라기보다 "뼈대(PARA) + 신경망(MOC)"에 가깝다고 이해하고 있습니다.

---

### 1. PARA 폴더로 정리할까, 링크로만 연결할까?

리서치 과정에서 실제로 상반된 조언을 발견했습니다. 한쪽(Second Brain 템플릿 판매 사이트인 obsibrain.com)은 PARA의 폴더 구조를 그대로 옵시디언에 옮겨 `00-inbox/`, `01-projects/`, `02-areas/`, `03-resources/`, `04-archive/` 형태로 쓰라고 권합니다. 반대로 다른 개인 블로그(mattgiaro.com, 발행 시점 불명이나 본문 스크린샷이 2022년 11월 것이어서 다소 오래된 정보일 수 있음)는 "PARA는 옵시디언에 권장되지 않는다"며 폴더 유지보수가 번거롭고 창의성을 제한한다고 반박합니다.

**폴더만 고집할 때 (문제점):** 폴더 트리가 깊어질수록 "이 노트를 어느 폴더에 넣을지" 고민하는 시간이 늘고, 나중에 옮기면 링크가 깨지기 쉽습니다.
**링크 + 얕은 폴더를 함께 쓸 때 (해결책):** 여러 소스에서 반복적으로 확인되는 실전 팁은 "PARA는 옵시디언에서 그냥 4개의 최상위 폴더일 뿐이며, 링크가 잘 갖춰져 있다면 깊은 폴더 트리보다 평평한(flat) PARA 구조 + 좋은 링크 조합이 낫다"는 것입니다. 저도 본인 기준으로는 이 쪽에 더 무게를 두고 있는데, 폴더는 최소한의 뼈대로만 쓰고 실제 탐색은 그래프뷰와 링크에 맡기는 편이 유지보수 부담이 훨씬 적었습니다.

![옵시디언 볼트 루트의 PARA 유사 폴더 구조(1_Project, 2_Break, 3_Create, 4_Portfolio, 5_Claude 등) 스크린샷](./images/body-2.png)

### 2. 그래프뷰가 저절로 연결되게 만드는 플러그인 조합

MOC를 "수동으로" 유지보수하려면 새 노트를 만들 때마다 상위 허브 노트에 링크를 걸어줘야 하는데, 노트가 많아지면 이게 은근히 귀찮은 작업입니다. 이걸 자동화해주는 조합이 **Folder Notes** + **Templater** + **Zoottelkeeper** 세 플러그인입니다.

**세 플러그인을 안 쓸 때 (문제점):** 폴더를 만들 때마다 대표 노트를 손으로 만들고, 그 안에 하위 파일 링크 목록을 일일이 추가·삭제해야 합니다. 파일이 이동되면 인덱스도 손으로 고쳐야 하니 그래프뷰에 고립 노드가 계속 생깁니다.

**세 플러그인을 함께 쓸 때 (해결책):**
- **Folder Notes**(개발자 Lost Paul): 폴더 자체에 노트를 붙여, 폴더명을 클릭하는 것만으로 그 폴더를 설명하는 노트를 열 수 있게 해줍니다. 설정에서 "새 폴더 생성 시 폴더 노트 자동 생성"(autoCreate)을 켜두면 폴더를 만드는 순간 노트가 자동 생성됩니다.
- **Templater**(개발자 SilentVoid13): 그렇게 자동 생성된 폴더 노트에 `title`, `updated`, `tags: [MOC]` 같은 frontmatter를 자동으로 채워주는 템플릿 엔진입니다. "현재 파일 제목이 소속 폴더 이름과 같을 때만"(진짜 폴더 노트일 때만) Zoottelkeeper용 마커를 조건부로 삽입하는 스크립트도 짤 수 있습니다.
- **Zoottelkeeper**(개발자 akosbalasko): 그 마커 사이 공간을 폴더 안의 모든 하위 파일·하위 폴더 링크 목록으로 자동으로 채우고, 파일이 추가·삭제·이동될 때마다 동적으로 갱신해줍니다. 원래 Nick Milo의 LYT/MOC 개념에서 영감을 받아 만들어진 플러그인이라고 공식적으로 소개돼 있습니다.

![Templater의 Folder Templates 설정 화면 - 폴더별 템플릿 매핑 예시](./images/body-3.png)

세 플러그인이 각자 역할을 나눠 맡는 구조입니다. Folder Notes가 "노트-폴더 매핑과 템플릿 적용"을, Templater가 "frontmatter와 조건부 마커 삽입"을, Zoottelkeeper가 "실제 링크 목록 채우기"를 담당합니다.

---

## 내 볼트(oortcloud)에 적용해본 후기

실제로 제가 쓰고 있는 옵시디언 볼트에 이 조합을 적용해봤습니다. 볼트 루트는 PARA와 비슷하게 `1_Project`, `2_Break`, `3_Create`, `4_Portfolio`, `5_Claude`, 날적이(다이어리), `Study`, `Templates` 같은 번호 붙은 최상위 폴더로 구성돼 있습니다.

### 1. 수동 링크 관리에서 해방

동작 순서는 이렇습니다. ① Folder Notes가 폴더마다 폴더명과 같은 이름의 노트를 autoCreate 옵션으로 자동 생성하고, ② 그 노트에 지정된 Templater 템플릿이 스켈레톤으로 적용되면서 frontmatter와 Zoottelkeeper 마커를 조건부로 삽입하고, ③ Zoottelkeeper가 그 마커 사이를 하위 파일·폴더의 위키링크 목록으로 채워 넣습니다. 이 과정이 볼트 루트부터 리프 노트까지(최소 3~4단계 깊이, 예: 루트 → `1_Project` → `Color_Brick` → 개별 노트) 재귀적으로 일어나기 때문에, 손으로 링크를 걸지 않아도 볼트 전체가 그래프뷰에서 하나의 연결망으로 묶입니다. 체감상 노트를 새로 쓸 때 "이걸 어디에 연결해야 하지"라는 고민 자체가 거의 사라졌습니다.

![Folder Notes+Templater+Zoottelkeeper 조합 적용 후 그래프뷰 - 노드들이 하나의 연결망으로 묶인 모습](./images/body-4.png)

### 2. 남은 과제 — 빈 폴더와 유지보수 리스크

다만 실사용 중에 걸리는 부분도 있었습니다. 아직 파일이 하나도 없는 빈 폴더는 상위 폴더 노트의 자동 인덱스 목록에는 이름이 올라가지만, 정작 그 폴더 안에는 폴더 노트 파일 자체가 생성되지 않은 상태라서 그래프뷰에서 "끊어진 링크(unresolved link)"로 표시됩니다. 폴더 안에 파일을 하나라도 만들거나, 옵시디언에서 그 폴더를 한 번 열어 폴더 노트 생성을 트리거하면 해결되긴 하지만, 매번 신경 써야 하는 부분이라 완전 자동화라고 하기엔 아쉬운 지점입니다.

![빈 폴더가 그래프뷰에서 끊어진 링크(unresolved link)로 표시되는 예시](./images/body-5.png)

---

## 결론 및 실무적 고려 사항

정리하면, **PARA**는 정보를 실행 가능성 기준으로 나누는 최소한의 폴더 뼈대를, **LYT/MOC**는 그 위에서 노트를 실제로 연결하는 신경망 역할을 합니다. 옵시디언에서는 폴더를 최대한 얕게 유지하고 링크로 연결을 촘촘히 만드는 쪽이 여러 소스에서 공통적으로 권장되는 방향이었고, 저도 본인 기준으로는 이 방식이 유지보수 부담이 적다고 체감했습니다. 자동화까지 원한다면 **Folder Notes + Templater + Zoottelkeeper** 조합이 실전에서 검증된 선택지입니다.

다만 한계도 분명합니다. Zoottelkeeper는 2026년 7월 기준 obsidianstats.com 집계로 마지막 릴리스가 2022년 3월(약 4년 전)이라, 옵시디언 코어 업데이트와의 호환성이 언제 깨질지 모른다는 유지보수 리스크를 안고 갑니다. 반면 같은 조합 안의 Folder Notes(약 1개월 전 업데이트)와 Templater(8일 전 업데이트, 누적 다운로드 470만 회 이상)는 활발히 관리되고 있어서, 세 플러그인의 유지보수 상태가 균일하지 않다는 점은 미리 감안해야 합니다. 또한 빈 폴더의 unresolved link 이슈처럼 완전히 손을 뗄 수는 없는 잔손질도 남아 있어서, "설정만 해두면 100% 자동"이라기보다 "수동 작업을 90% 이상 줄여주는 도구"로 기대치를 잡는 게 맞다고 봅니다.

---
*참고: [GitHub - akosbalasko/zoottelkeeper-obsidian-plugin](https://github.com/akosbalasko/zoottelkeeper-obsidian-plugin), [Zoottelkeeper – Obsidian Plugin · Obsidian Stats](https://www.obsidianstats.com/plugins/zoottelkeeper-obsidian-plugin), [GitHub - LostPaul/obsidian-folder-notes](https://github.com/LostPaul/obsidian-folder-notes), [Folder Notes – Obsidian Plugin · Obsidian Stats](https://www.obsidianstats.com/plugins/folder-notes), [GitHub - SilentVoid13/Templater](https://github.com/SilentVoid13/Templater), [Templater – Obsidian Plugin · Obsidian Stats](https://www.obsidianstats.com/plugins/templater-obsidian), [Building a Second Brain: The Definitive Introductory Guide - Forte Labs](https://fortelabs.com/blog/basboverview/), [Linking Your Thinking 공식 사이트](https://www.linkingyourthinking.com/), [How to Build a Second Brain in Obsidian - mattgiaro.com](https://mattgiaro.com/second-brain-obsidian/)*

<!--
게시 전 체크 (naver-seo-guide.md / google-guide.md 반영 메모, 발행 시 삭제 가능)

[제목] 글자수·키워드 위치·특수문자 여부 점검
[본문 분량] 공백 제외 글자수 / 단어수 기록
[키워드 배치] 사용한 핵심 키워드와 배치 위치 요약
[이미지] [IMAGE: ...] 자리 개수와 실제 촬영/제작 필요 여부
[네이버 해시태그] #태그 3~4개 후보
[구글] description 글자수 확인, JSON-LD는 Jekyll SEO tag가 front matter 기반으로 자동 생성됨
[애드센스] 광고 삽입 권장 위치 (첫 문단 앞 배치 금지) 메모
-->
