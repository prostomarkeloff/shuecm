from mongodb_migrations.base import BaseMigration

# get time for name file - `date +%s` in your shell.


class Migration(BaseMigration):
    def upgrade(self):
        for item in self.db.user_in_chat.find():
            item["warns"] = 0
            self.db.user_in_chat.save(item)

    def downgrade(self):
        self.db.user_in_chat.update_many({}, {"$unset": {"warns": 0}})
