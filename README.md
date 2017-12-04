# 生体情報学の実験画像を自動で生成する奴

##### 先にやっておいてほしいこと

各実験のcsvの結果ファイルのcsvのヘッダが書かれている1行目を削除する．(skipcolが仕事しなかった，何もわからん.)
clone後にinit.shを実行する．ディレクトリ内に実験番号に対応した`[1-7]/`が生成されるのでその中に加工した実験回数に対応した`[1-5].csv`を入れる．

### 使い方

##### 最小実行
```
$ git@github.com:Knium/seitai-joho.git
$ cd seitai-joho
$ sh init.sh
$ ./cli.py -f <path/to/font>
```

##### ある実験の第3~5回目だけの画像を生成する
`$ ./cli.py -f <path/to/font> -r 3 5`

##### パワースペクトルの画像のみを生成する
`$ ./cli.py -f <path/to/font> -s`