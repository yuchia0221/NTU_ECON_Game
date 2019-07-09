<h1>伊康攻略</h1>


<h3>規則說明</h3>
<h5>勝利條件</h5>
<ul>
  <li>Wonder = 世界奇觀貢獻度, Gold = 黃金存量, Asset = 四項基礎物資總和</li>
  <li>總積分 = 200 * Wonder2 + 1000 * Wonder + Gold + 0.5 * Asset</li>
</ul>

<h5>遊戲流程</h5>
<ul>
  <li>用餐時間依序提交表單(系統貿易單、行動單)，約10 回合(依時間調整)。</li>
  <li>第二回合開始才能【系統貿易】，第三回合開始才能【戰爭】。</li>
  <li>可以透過支線活動獲得獎勵，獎勵內容會在活動前公布。</li>
  <li>小隊呈現有最後的Bonus !</li>
  <li>排名隨時更新，於結業式結算及頒獎。</li>
  <li>行動執行順序: 系統貿易 → 生產 → 投資 → 教育 → 戰爭 → 世界奇觀 → 消耗</li>
  <li>特殊事件會不定期的發生哦，要隨時做好應變工作。</li>
</ul>

<h3>程式說明</h3>
<h5>使用函式庫</h5>
<ul>
  <li>gspread</li>
  <li>collections</li>
  <li>random</li>
  <li>time/li>
  <li>pandas</li>
</ul>
<p>透過gspread與google雲端連結，抓取玩家的行動資訊(回應表單)，利用Python在本地端跑完數據在更新上去雲端</p>
