# AI Character LINE Bot

デモ動画：https://youtube.com/shorts/IX3m62dwLvE?feature=share

## 概要 (Overview)
このプロジェクトは、LINEプラットフォーム上で動作する対話型AIボットです。ユーザーは、キャラクターになりきったAIと雑談を通じて、ちょっとした癒しや楽しみを得ることができます。

### 主な機能 (Key Features)
- 🎭 キャラクターロールプレイ: AIが特定のキャラクターとして応答
- 💬 自然な会話: 文脈を理解した自然な対話が可能
- 🔄 リアルタイムレスポンス: ユーザーのメッセージにすぐに応答
- 📝 会話履歴の保持: 文脈を考慮した応答が可能

### 技術スタック (Tech Stack)
- 🐍 Backend: Python (FastAPI)
- 🤖 AI: OpenAI API
- 💬 Messaging: LINE Messaging API
- 🐳 Container: Docker




## 改善計画（Improvement Plan）

### 1. アーキテクチャと設計
- [ ] クリーンアーキテクチャの導入
  - [ ] レイヤー分離（Presentation, Domain, Infrastructure）
  - [ ] Repository パターンの実装
  - [ ] UseCase（Application Service）レイヤーの追加
  - [ ] 依存性の注入（DI）の導入

### 2. データベース
- [ ] ローカルDB環境の構築
  - [ ] PostgreSQL/MySQLの導入
  - [ ] マイグレーション管理（Alembic）
  - [ ] DBバックアップ戦略
  - [ ] データベースのDockerコンテナ化
- [ ] ORMの活用（SQLAlchemy）
  - [ ] モデル定義
  - [ ] リレーション設計

### 3. コード品質
- [ ] 静的解析ツールの導入
  - [ ] mypy（型チェック）
  - [ ] black（コードフォーマッター）
  - [ ] isort（import文の整理）
  - [ ] flake8（コードスタイルチェック）
  - [ ] pylint（コード品質チェック）
- [ ] pre-commit hooksの設定
  - [ ] コミット前の自動フォーマット
  - [ ] リントチェック

### 4. テスト
- [ ] テストフレームワークの導入
  - [ ] pytest
  - [ ] pytest-cov（カバレッジレポート）
- [ ] テストの種類
  - [ ] 単体テスト
  - [ ] 統合テスト
  - [ ] E2Eテスト
- [ ] モック/スタブの活用
  - [ ] LINE API のモック
  - [ ] DBのモック

### 5. CI/CD (GitHub Actions)
- [ ] CI パイプライン
  - [ ] コードの静的解析
  - [ ] テストの自動実行
  - [ ] カバレッジレポート生成
  - [ ] セキュリティスキャン
- [ ] CD パイプライン
  - [ ] AWS環境へのデプロイ
  - [ ] インフラのプロビジョニング（Terraform）
  - [ ] ブルー/グリーンデプロイメント

### 6. インフラストラクチャ
- [ ] AWS環境の整備
  - [ ] Lambda関数の設定
  - [ ] API Gatewayの設定
  - [ ] Bedrockの統合
- [ ] Terraformによるインフラのコード化
  - [ ] 環境ごとの設定分離
  - [ ] 状態管理（tfstate）

### 7. セキュリティ
- [ ] シークレット管理
  - [ ] AWS Secrets Managerの活用
  - [ ] 環境変数の適切な管理
- [ ] セキュリティスキャン
  - [ ] dependabotの設定
  - [ ] SAST（静的アプリケーションセキュリティテスト）
- [ ] アクセス制御
  - [ ] IAMポリシーの最小権限原則
  - [ ] API認証/認可

### 8. モニタリングとロギング
- [ ] ログ管理
  - [ ] CloudWatch Logsの設定
  - [ ] 構造化ログの導入
- [ ] メトリクス収集
  - [ ] CloudWatch Metricsの設定
  - [ ] カスタムメトリクスの追加
- [ ] アラート設定
  - [ ] エラー通知
  - [ ] パフォーマンス監視

### 9. ドキュメント
- [ ] API仕様書
  - [ ] OpenAPI (Swagger)の導入
- [ ] アーキテクチャ図
- [ ] セットアップガイド
- [ ] 運用マニュアル

### 10. パフォーマンス最適化
- [ ] キャッシュ戦略
- [ ] N+1問題の解決
- [ ] クエリの最適化
- [ ] レスポンスタイムの改善

### 11. 開発環境
- [ ] Docker開発環境の改善
  - [ ] マルチステージビルド
  - [ ] 開発/本番環境の分離
- [ ] VSCode設定
  - [ ] デバッグ設定
  - [ ] 推奨拡張機能
