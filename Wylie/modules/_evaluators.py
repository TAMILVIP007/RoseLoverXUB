from Wylie.events import Wbot
from Wylie import ubot, tbot
import subprocess, asyncio, traceback, io, sys, os, time
import requests

@Wbot(pattern="^/exec ?(.*)")
async def ebent(event):
    if event.fwd_from:
        return
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.edit("What should i execute?..")
    catevent = await event.edit("Executing.....")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    curruser = "RoseLoverX"
    uid = os.geteuid()
    if uid == 0:
        cresult = f"`{curruser}:~#` `{cmd}`\n`{result}`"
    else:
        cresult = f"`{curruser}:~$` `{cmd}`\n`{result}`"
    await catevent.edit(cresult)
    
    
@Wbot(pattern="^/eval ?(.*)")
async def ubot(event):
    if event.fwd_from:
        return
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return
    catevent= await event.edit("Running ...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**•  Eval : **\n`{cmd}` \n\n**•  Result : **\n`{evaluation}` \n"
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await ubot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )
    else:
        await catevent.edit(final_output)

async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, ubot, p)


@Wbot(pattern="^/go ?(.*)")
async def go(event):
 args = event.pattern_match.group(1)
 await event.edit("Excecuting...")
 data = {
        "code": args,
        "lang": 'go',
        "token": "5b5f0ad8-705a-4118-87d4-c0ca29939aed",
    }
 
 r = requests.post("https://starkapis.herokuapp.com/compiler", data=data).json()
 if r.get("reason") != None:
        result = f"""**Code:** \n`{reply_code}` 
**Result:** 
`{r.get("results")}`
**Error:** 
`{r.get("errors")}`
**Stats:**
 `{r.get("stats")}`
**Success:** 
 `{r.get("success")}`
**Warnings:** 
 `{r.get("warnings")}`
**Reason:**
 `{r.get("reason")}`
 """
 else:
        result = f"""**Code:** \n`{reply_code}` 
**Result:** 
`{r.get("results")}`
**Error:** 
`{r.get("errors")}`
**Stats:**
 `{r.get("stats")}`
**Success:** 
 `{r.get("success")}`
**Warnings:** 
 `{r.get("warnings")}`
 """
 await event.edit(result)
 
