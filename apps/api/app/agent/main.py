from .app import create_agent


if __name__ == "main":
    agent = create_agent()

    print(agent.config.get("app_name"))

    # gw = app.get(ArmyPainter)
    # wf = await gw.get('sprays') # , from_fs=True

    # print(len(wf.products))

    # categories = gw.scrape_plp('speedpaint')
