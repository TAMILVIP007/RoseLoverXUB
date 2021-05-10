from Wylie.events import Wbot

UPSTREAM_REPO_URL = "https://github.com/AmarnathCjd/RoseLoverXUB"
from os import remove, execle, path, environ
import asyncio
import sys
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"•[{c.committed_datetime.strftime(d_form)}]: {c.summary} by <{c.author}>\n"
        )
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)
      
@Wbot(pattern="^/update ?(.*)")
async def _(ups):
    lol = await ups.edit("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "`Oops.. Updater cannot continue "
        repo = Repo()
    except NoSuchPathError as error:
        await lol.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await lol.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != "master":
        await lol.edit(
            f"**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        repo.__del__()
        return

    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if not changelog and not force_update:
        await lol.edit("\n`Your bot is`  **up-to-date**  \n")
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = (
            f"**New UPDATE available for {ac_br}\n\nCHANGELOG:**\n`{changelog}`"
        )
        if len(changelog_str) > 4096:
            await lol.edit("`Changelog is too big, view the file to see it.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await tbot.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await lol.edit(changelog_str + "\n\n" + "**do** `/update now` **to update**")

        return

    if force_update:
        await lol.edit("`Force-Syncing to latest master bot code, please wait...`")
    else:
        await lol.edit("`Still Running ....`")
    try:
            ups_rem.pull(ac_br)
    except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
    reqs_upgrade = await updateme_requirements()
    await lol.edit("`Successfully Updated!\n" "restarting......`")
    args = [sys.executable, "-m", "Wylia"]
    execle(sys.executable, *args, environ)
    return
