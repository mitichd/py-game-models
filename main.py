import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as file:
        players_data = json.load(file)

    for nickname, player_data in players_data.items():
        if Player.objects.filter(nickname=nickname).exists():
            continue

        race_data = player_data.get("race", {})
        race = Race.objects.filter(name=race_data.get("name")).first()
        if not race:
            continue

        guild_data = player_data.get("guild", {})
        guild = None
        if guild_data:
            guild = Guild.objects.filter(name=guild_data.get("name")).first()
            if not guild:
                continue

        skills = []
        for skill_data in race_data.get("skills", []):
            skill_name = skill_data.get("name")
            if skill_name:
                skill = Skill.objects.filter(name=skill_name).first()
                if skill:
                    skills.append(skill)

        Player.objects.create(
            nickname=nickname,
            email=player_data.get("email"),
            bio=player_data.get("bio"),
            race=race,
            guild=guild,
        )


if __name__ == "__main__":
    main()
