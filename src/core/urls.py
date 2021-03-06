from django.conf.urls import patterns, include, url


task_patterns = patterns("core.views",
    url(
        '^resync-player-match-counts/',
        'resync_player_match_counts',
        name="resync_player_match_counts"
    ),
    url(
        '^reset-challenges/',
        'reset_challenge_instances',
        name="reset_challenge_instances"
    ),
    url(
        '^recalculate-elo/',
        'recalculate_player_elo_ratings',
        name="recalculate_player_elo_ratings"
    ),
    url(
        '^set-active-flag/',
        'set_active_player_flag',
        name="set_active_player_flag"
    ),
    url(
        '^resync-player-granny-count/',
        'resync_player_granny_counts',
        name="resync_player_granny_count"
    ),
    url(
        '^migrate-season-fields/',
        'season_migration',
        name="season_migration"
    ),
    url(
        '^set-active-season/',
        'set_active_season',
        name="set_active_season"
    ),
    url(
        '^migrate-elo-history',
        'elo_history_migration',
        name='elo_history_migration'
    ),
    url(
        '^migration-season-player',
        'season_player_migration',
        name='season_player_migration'
    ),
    url(
        '^update-slack-fields',
        'update_slack_player_fields',
        name='update_slack_fields'
    ),
)


urlpatterns = patterns('',
    url(r"^", include(task_patterns)),
)
