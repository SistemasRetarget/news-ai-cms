class CreateFeedbacks < ActiveRecord::Migration[7.0]
  def change
    create_table :feedbacks do |t|
      t.references :user, null: false, foreign_key: true
      t.integer :feedback_type, default: 0
      t.text :content
      t.jsonb :data, default: {}

      t.timestamps
    end

    add_index :feedbacks, :feedback_type
    add_index :feedbacks, :created_at
  end
end
