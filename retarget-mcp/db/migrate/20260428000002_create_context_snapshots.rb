class CreateContextSnapshots < ActiveRecord::Migration[7.0]
  def change
    create_table :context_snapshots do |t|
      t.references :user, null: false, foreign_key: true
      t.jsonb :data, default: {}

      t.timestamps
    end

    add_index :context_snapshots, :created_at
  end
end
