import requests
from lxml import html, etree
import discord
import shutil
from discord.ext import commands
from key import token #create file key.py file with token='Ur token'
import os.path
import time
from PIL import Image
mainurl="https://distrowatch.com/"

async def search(distro):
    try:
        output={}
        page = requests.get('https://distrowatch.com/table.php?distribution=%s'%distro.replace(" ", "+"))
        tree = html.fromstring(page.content)
        output["ss"] = mainurl+tree.xpath("//td[@class='TablesTitle']/a/img")[0].attrib["src"]
        output["logo"] = mainurl+tree.xpath("//td[@class='TablesTitle']/img")[0].attrib["src"]
        output["Name"] = tree.xpath("//td[@class='TablesTitle']/h1")[0].text
        output["OS-Type"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[0].text_content()
        output["Based-on"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[1].text_content()
        output["Origin"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[2].text_content()
        output["Architecture"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[3].text_content()
        output["Desktop"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[4].text_content()
        output["Category"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[5].text_content()
        output["Status"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[6].text_content()
        output["Popularity"]= tree.xpath("//td[@class='TablesTitle']/ul/li")[7].text_content()
        return output
    except:
        return None

async def send_picture(ctx, info, key):
    fpath='/tmp/'+info["Name"]+'-'+key+'.png'
    if (not os.path.isfile(fpath)):
        img = requests.get(info[key], stream=True)
        with open(fpath, 'wb') as out_file:
            shutil.copyfileobj(img.raw, out_file)
            del img
        pic = Image.open(fpath).convert('RGBA')
        Image.alpha_composite(Image.new('RGBA', pic.size, (255,255,255)), pic)\
            .save(fpath, 'PNG', quality=80)
    await ctx.send(file=discord.File(fpath, 'new_filename.png'))
    return None


bot = commands.Bot(command_prefix='?')
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('using discord.py %s'%discord.__version__)
@bot.command(pass_context=True)
async def distro(ctx, name):
    start_time=time.time()
    response = await search(name)
    #print(response)
    if (response):
        output_pattern=["OS-Type","Based-on","Origin","Architecture","Desktop","Category","Status","Popularity"]
        await send_picture(ctx, response, "logo")
        await ctx.send(response["Name"])
        specs = ["******* "]
        for key in output_pattern:
            specs.append(response[key].replace("\n", ""))
        print(specs)
        await ctx.send("\n".join(specs))
        await send_picture(ctx, response, "ss")
    else:
        await ctx.send("Could not find that distro. Are you sure you're not trying to search for some shady OS from Microsoft?")
    await ctx.send("It took {:.2f}s to return".format(time.time()-start_time))
            
bot.run(token)