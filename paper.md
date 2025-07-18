# ブロックチェーン決済チャネルネットワークにおけるプライバシー・レイテンシジレンマを解決するルーティング手法

## 著者
**佐藤 衡平**  
芝浦工業大学 理工学研究科  
東京，日本  
af20023@shibaura-it.ac.jp

**森野 博章**  
芝浦工業大学 理工学研究科  
東京，日本  
morino@shibaura-it.ac.jp

## 概要
本稿では、グループ化された決済チャネルの最小容量のみを開示するGroup Capacity Broadcasting（GCB）手法を提案する。これにより、プライバシーを保護しながら決済の再試行を減らすことができる。
実際のLightning Networkのスナップショットを用いたシミュレーション結果により、GCBが従来手法と比較して成功率を犠牲にすることなく決済確認遅延を大幅に削減することを実証した。
本手法は特に大額決済において効果的であり、従来の確率的ルーティングでは多くの再試行と長時間の確認時間を要していた問題を解決する。

## キーワード
ブロックチェーン、決済チャネルネットワーク、ルーティング手法、ゴシッププロトコル

## 1. はじめに

複数の決済チャネルを接続したPayment Channel Networks（PCN）は、ブロックチェーンのスケーラビリティ問題の解決策として近年注目を集めている。
決済チャネルは、将来の取引のために十分な資金をコミットする2つの参加者によって作成される。
資金はブロックチェーンアドレスに送金され、両参加者の合意によってのみアンロックできる。
コミットされた資金の総額はチャネル容量と呼ばれ、ブロックチェーン上で公開される。
決済チャネル内での支払いは、各参加者の資金の取り分であるバランスを更新することで実行されるが、これらの変更はブロックチェーンに記録されず、即座の決済処理を可能にする。

複数の決済チャネルを接続して構築されたネットワークは、Payment Channel Network（PCN）と呼ばれる。
PCNでは、送信者は直接接続されていない受信者に対して、HTLCsと呼ばれるスクリプトベースの取引を用いて複数の決済チャネルを通じて安全かつ迅速に資金を転送できる。
PCNは高速な決済処理を提供するだけでなく、ブロックチェーンでは利用できない独特な機能も提供する：決済チャネル参加者のバランスは公開されないため、送信者、受信者、決済額などの決済情報は無関係な第三者から隠される。

PCNユーザーを有向グラフのノードとして、決済チャネルを双方向リンクとしてモデル化すると、各チャネルの各参加者のバランスは、その参加者を開始ノードとするリンクの容量に対応する。
また、取引手数料はリンクコストに対応する。
各決済チャネルの参加者のバランスを超える決済額を送信することは不可能である。
つまり、従来の通信ネットワークとは異なり、決済チャネルの両方向のリンクの容量の合計は常にチャネル容量と等しく一定であり、決済が行われるたびに各方向の容量が変化する。
また、各参加者の決済チャネルのバランスは他のチャネルの関係者には開示されない。
その結果、送信者は経路上のリンク容量の情報なしに決済経路を決定し、決済を試行しなければならないため、経路上の一部のリンクの容量が決済額より小さい場合に決済試行が失敗することが多い。この場合、成功するまで代替経路を使用して試行が再試行され、決済に追加の遅延が発生する。

重要なジレンマが発生する：決済チャネルは多数の取引をオフチェーンに移すことでブロックチェーンのスケーリングに効果的であるが、送信者はすべてのリンクが十分な容量を持つ経路を選択しなければならない。

各リンクが現在のバランスを公開すれば、送信者は最初の試行で実行可能な経路を選択できるが、外部の観察者が決済を追跡できるためプライバシーが失われる。
バランスが秘密のままであれば、プライバシーは保護されるが、決済失敗が頻繁に発生し、前述のように決済再試行と長い遅延が発生する。
Lightning Networkの確率的ルーティングは遅延を若干緩和するが、大額決済では依然として困難である。

本稿では、プライバシー・レイテンシジレンマに対処する。
リンクグループ内の最小バランスのみを開示し、個々のバランスを隠しながら送信者が事前に実行不可能な経路を除外できるGroup Capacity Broadcasting（GCB）手法を提案する。

## 2. GCB手法

GCB手法では、互いに近い容量を持つ複数のリンクがグループを形成し、メンバーリンクの最小容量のみをブロードキャストする。
具体的なプロセスは以下の通りである。
グループ構築者は、容量範囲[`min_cap_limit`, `max_cap_limit`]を指定する`group_req`メッセージをブロードキャストしてリンクを募集する。
`group_size`数のリンクが参加すると、グループは個々のリンクバランスを公開することなく最小容量を計算する。

重要な革新は、プライバシー保護最小値発見プロトコルである。
各グループメンバーリンク（より正確には、各リンクの開始ノード）は、実際の容量と一意の識別子を含む`group_cap`メッセージを作成し、すべてのメンバーが参加し、メッセージの損失を防ぐためにリング形式でグループのすべてのメンバーにメッセージを循環させる。
メッセージが各ノードを通過する際、リンクの容量がより小さい場合にのみメッセージ内の容量値が更新され、最終結果が真の最小値を表すことを保証する。
各ノードや外部の観察者が他の特定のリンクの容量を知ることを防ぎ、リンク容量の匿名性を維持するため、ノードは確率的な難読化を実行する。
循環中に容量が小さくても、約半分の確率でランダムにメッセージの更新を控える。
これにより、更新の不在が必ずしもノードの実際の容量が変化していないことを意味しないため、グループ内の各ノードはどのノードが容量更新を引き起こしたかを判断できない。
メッセージが循環を完了した後、ノードが自分のメッセージ識別子を受信すると、最小値の有効性を認識し、`group_update`メッセージとしてネットワーク全体にブロードキャストする。
この分散合意メカニズムにより、単一のノードが実際に最小容量を保持するリンクを特定できないことを保証し、決済プライバシーを維持する。
図1はこのプロトコルの詳細なメッセージフローを示している。

ルーティング決定において、送信者は開示されたグループ容量が保守的な下限を表すため、送信前に経路の実行可能性を判断できる。
これは、グループ内の各個別リンクの真の容量が、開示されたグループ容量以上であることが保証されることを意味する。
送信者は、グループ化されたリンクにはグループ容量を、グループ化されていないリンクにはチャネル容量を使用し、標準的な最短経路アルゴリズムを適用する。
決済成功後、影響を受けたグループは匿名性を保持しながら精度を維持するため、バランス変更を反映して最小容量を再計算する。

グループ容量更新プロセス中の確率的難読化メカニズムにより、特定のリンク容量の変更が公開されないため、プライバシーが保護される。
グループ容量の値が指定された範囲を超えるとグループは閉鎖され、変化するネットワーク条件に適応するため、異なるパラメータを持つ新しいグループに参加する。

![図1: グループ容量計算プロトコルメッセージフロー](fig/group_cap_handover.pdf)

## 3. 性能評価

本節では、シミュレーションを通じて提案するGCB手法のレイテンシ性能を評価する。ここでレイテンシは、決済開始から決済確認（成功・失敗に関わらず）までの経過時間として定義する。

### 3.1 シミュレーション条件
Lightning Network HTLCsを正確に再現するPCNシミュレータCLoTHを拡張し、GCB手法を実装した。
2020年12月17日のLightning Networkスナップショットを使用し、6,005ノードと60,913リンクを含む。
このデータはLNDの`describegraph`コマンドから取得し、実際のネットワークで利用可能な公開情報と同一の情報をすべて含む。
初期決済チャネルバランスは公開されていないため、一様分布ランダム値を使用して設定した。
正規分布に従う決済額（平均μ = 10,000サトシ、分散σ = μ × 0.1）で5,000回の決済を実行し、送信者と受信者を一様分布ランダム選択した。

### 3.2 レイテンシ評価

決済額を変化させて、提案するGCB手法と従来のLightning Network確率的ルーティング手法を比較した。
結果は、従来手法の確認遅延が決済額とともに大幅に増加するのに対し、GCB手法の遅延は比較的少ない増加を示した。
大額決済において、従来手法は実際のリンク容量の情報を持たず、過去の失敗頻度のみでリンクの利用可能性を判断するため多くの再試行を経験し、確認時間が長期化する。
GCB手法は保守的な容量境界を開示することで不要な再試行を排除し、実行不可能な決済の送信前即座判定を可能にし、図2で示すように大額でも確認遅延の増加を最小限に抑える。

![図2: 成功ケースのみにおける決済送信レイテンシ vs 決済額](fig/pmt_amt_vs_time.pdf)

## 参考文献

[1] J. Poon and T. Dryja, "The bitcoin lightning network: Scalable off-chain instant payments," 2016.

[2] S. Nakamoto, "Bitcoin: A peer-to-peer electronic cash system," 2008.

[3] "BOLT: Basis of Lightning Technology," https://github.com/lightningnetwork/lightning-rfc.

[4] "Lightning Network Daemon," https://github.com/lightningnetwork/lnd.

[5] "Core Lightning," https://github.com/ElementsProject/lightning.

[6] "Eclair," https://github.com/ACINQ/eclair.

[7] M. Conoscenti et al., "CLoTH: A simulator for HTLC payment networks," Future Generation Computer Systems, vol. 118, pp. 1--17, 2021. 