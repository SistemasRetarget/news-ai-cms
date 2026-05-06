class CreateUsers < ActiveRecord::Migration[7.0]
  def change
    create_table :users do |t|
      t.string :email, null: false
      t.string :name
      t.integer :role, default: 0
      t.integer :ai_tool, default: 0
      t.boolean :is_ai_user, default: false
      t.boolean :active, default: true

      t.timestamps
    end

    add_index :users, :email, unique: true
  end
end
