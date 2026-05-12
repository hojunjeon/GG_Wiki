---
source: geeknews
date: 2026-05-11
points: 15
url: "https://news.hada.io/topic?id=29408"
title: "Show GN: 3초 만에 동기화하는 오픈소스 Obsidian 플러그인"
---

# Show GN: 3초 만에 동기화하는 오픈소스 Obsidian 플러그인

Show GN: 3초 만에 동기화하는 오픈소스 Obsidian 플러그인
(synch.run)Obsidian용 오픈소스 동기화 플러그인 Synch를 만들고 있습니다.
Obsidian Sync 같은 경험을 오픈소스로 만들 수 있을까 해서 시작했습니다.
목표는 빠른 동기화, E2EE, 버전 히스토리, 직접 배포 가능한 Obsidian Sync 대안입니다.
옵시디언 플러그인 방식이라 별도 앱을 설치하는 방식이 아니라 Obsidian이 동작하는 데스크톱/모바일 환경에서 사용할 수 있습니다.
현재 지원하는 기능은 다음과 같습니다.
- 파일 내용과 경로 메타데이터를 로컬에서 암호화한 뒤 업로드
- 여러 기기 사이에서 몇 초 안에 변경사항 동기화
- 버전 히스토리
- 삭제 파일 복구
- 파일 충돌 시 자동 병합
기술적으로는 Cloudflare Workers + Durable Objects + R2 위에서 동작합니다.
- 클라이언트에서 파일 내용과 경로 메타데이터를 암호화한 뒤 업로드합니다.
- 서버는 암호화된 blob과 동기화 메타데이터만 저장합니다.
- Durable Objects는 vault 단위 동기화 상태와 변경 순서를 관리하는 데 사용하고 있습니다.
- 파일 본문과 버전 히스토리는 R2에 저장합니다.
직접 배포해보고 싶은 분들을 위해 Cloudflare 무료 계정으로 배포할 수 있는 원클릭 배포도 준비해두었습니다.
배포가 번거로운 분들은 hosted server로 먼저 간단히 테스트해볼 수 있습니다.
GitHub: https://github.com/hjinco/synch
셀프호스팅으로 계정을 생성했다가 동일 계정으로 로그인을 못하고 있어요
아마도 제가 패스워드를 잊은 실수겠죠^^
그런데 패스워드를 초기화하는 방법이 없네요
어쩔 수없이 github repo, workers 모두 삭제하고 다시 설정하고 있는데요
이번에는 이상하게도 회원가입할 때 이미 있는 계정이라고 나오네요..
아니요 그냥 cloudflare 계정만 있으면 됩니다. https://synch.run/ko/self-hosting 가이드 보시면 됩니다.
오~ 완성도가 꽤 있어 보이네요.
그런데 원격 볼트를 생성하고 동기화를 2개 기기에서 했더니 각각 폴더트리에 볼트 하나가 더 생기면서 그 아래 원래 폴더트리가 중복으로 생기네요. 원래 이렇게 되는건가요?
원래 그렇게 되는 동작은 아닙니다.
그 현상이 저나 베타 테스터분들께서는 재현되지 않았는데 괜찮으시면 contact@synch.run 으로 메일 주시거나 GitHub 이슈로 남겨주세요. 더 자세히 확인해보고 도와드리겠습니다.
vault를 삭제하려 했는데 오류가 발생하네요.
삭제 failed - coordinator purge failed with status 500