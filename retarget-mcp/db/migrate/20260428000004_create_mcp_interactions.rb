class CreateMcpInteractions < ActiveRecord::Migration[7.0]
  def change
    create_table :mcp_interactions do |t|
      t.references :user, null: false, foreign_key: true
      t.jsonb :data, default: {}

      t.timestamps
    end

    add_index :mcp_interactions, :created_at
  end
end
