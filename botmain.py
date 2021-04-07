import discord,os,random
from discord.ext import commands
import time
from money import Account
from game import *
from stockmodule import *

img_list = ["hole.png", "jjak.png"]

adminlist = ["Sgom#5840"]
TOKEN = os.getenv('DISCORD_TOKEN')
acc = Account()
game = Game(acc)
game_set = ["가위", "바위", "보"]
game_dict = {"가위" : 0, "바위": 1, "보": 2} 
hole_dict = {"홀" : 0, "짝": 1}

stock = Stock(acc)
client = discord.Client()
bot = commands.Bot(command_prefix='!')
sess = {}

@client.event
async def on_ready():
    print(client.user)

@bot.command(name="도움말")
async def manpage(ctx):
    string = "```---돈 관련---\n!돈, !시세, !매도, !매수, !송금, !도박, !랭킹, !31, !홀짝, !구제\n\n --QUIZ Evnet--\n !상점```"
    await ctx.send(string)
@bot.command(name="시세")
async def quote(ctx, *args):
    now = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    mseesage = "```" + now + "시간 기준" + "\nBTC: " + format(stock.getBTCinfo(), ",") + " KRW\n\n" +"ETH: " + format(stock.getETHinfo(), ",")+" KRW```"
    #await ctx.send("```"+now+"\n BTC:"+str(stock.getBTCinfo()) +"KRW```")
    await ctx.send(mseesage)
@bot.command(name="매수")
async def buy(ctx, *args):
    if len(args) != 2:
        await ctx.send("```css\n !매수 ETH,BTC <수량 소수점 매매 가능> (모두 시장가 매수 됩니다)```")
        return
    if args[0] not in stock.activemarket:
        await ctx.send(args[0]+"은 현재 지원하지 않습니다.")
        return
    if stock.buystock(str(ctx.author), args[0], float(args[1])):
        await ctx.send("```거래에 오류가 발생했습니다.```")
        return
        
    await ctx.send("```매수 성공```")
    
    
    
@bot.command(name="송금")
async def send(ctx, *args):
    if(len(args) != 2):
        await ctx.send("```!송금 사용자#3212 <금액>```")
        return
    if(acc.currentDepositI(str(ctx.author)) < int(args[1])):
        await ctx.send("```계좌 잔액보다 송금 금액이 많습니다.```")
        return
    
    acc.updateMoney(str(ctx.author), -int(args[1]))
    acc.updateMoney(str(args[0]), int(args[1]))
    await ctx.send("```송금에 성공 했습니다.```")
@bot.command(name="랭킹")
async def rank(ctx):
    data = acc.moneyRank()
    count = 1
    strbuilding = "```\n"
    for ranking in data:
        strbuilding += "%d. %s 잔액: %d\n" % (count, ranking[0], ranking[1])
        count += 1
    strbuilding += "```"
    await ctx.send(strbuilding)
@bot.command(name="매도")
async def sell(ctx, *args):
    if (len(args) != 2):
        await ctx.send("```\n!매도 BTC,ETH 수량```")
        return
    if stock.sellStock(str(ctx.author), args[0], float(args[1])) == -1:
        await ctx.send("```보유 수량 보다 많은 수량은 매도가 불가능 합니다. ```")
        return
    await ctx.send("```매도에 성공하셨습니다.```")
    
@bot.command(name="도박")
async def gamble(ctx, *args):
    if len(args) == 0:
        await ctx.send("```가위바위보 게임 입니다 !도박 <가위,바위,보> <배팅금액>\n 승리: 2.0\n 무승부: 1.0\n 패배: 0```")
        return
    if args[0] == "가위" or args[0] == "바위" or args[0] == "보":
        if len(args) == 1:
            await ctx.send("베팅 금액을 입력해주세요..")
            return
        if acc.search(str(ctx.author)) == []:
            await ctx.send("```우선 계좌를 생성해 주세요\n !돈```")
            return
        if int(args[1]) > 0:
            if (acc.currentDepositI(str(ctx.author)) < int(args[1])):
                await ctx.send("잔액이 부족합니다.")
                return
            await ctx.send("게임 진행중....")
            time.sleep(1.5)
            bot_dicsion = random.randrange(0,3)
            await ctx.send("BOT: " + str(game_set[bot_dicsion]))
            player_dicsion = game_dict[args[0]]
            if player_dicsion == bot_dicsion:
                await ctx.send("무승부 입니다")
                return
            elif player_dicsion == 0:
                if bot_dicsion == 1:
                    await ctx.send("안타깝네요.. 패배하셨습니다.")
                    result = 0
                elif bot_dicsion == 2:
                    await ctx.send("축하드립니다. 승리하셨습니다")
                    result = 1
            elif player_dicsion == 1:
                if bot_dicsion == 2:
                    await ctx.send("안타깝네요.. 패배하셨습니다.")
                    result = 0
                elif bot_dicsion == 0:
                    await ctx.send("축하드립니다. 승리하셨습니다")
                    result = 1
            elif player_dicsion == 2:
                if bot_dicsion == 0:
                    await ctx.send("안타깝네요.. 패배하셨습니다.")
                    result = 0
                elif bot_dicsion == 1:
                    await ctx.send("축하드립니다. 승리하셨습니다")
                    result = 1
            game.gameProcess(str(ctx.author), int(args[1]), result)
            await ctx.send(acc.currentDeposit(str(ctx.author)))

@bot.command(name='홀짝')
async def holejjak(ctx, *args):
    if acc.search(str(ctx.author)) == []:
        await ctx.send("```!돈 으로 계정을 생성해 주세요.```")
        return
    if len(args) == 0:
        await ctx.send("```!홀짝 <홀,짝> 배팅금액```")
        return
    if int(args[1]) < 0:
        await ctx.send("```음수 배팅은 불가능합니다..```")
    if int(args[1]) > acc.currentDepositI(str(ctx.author)):
        await ctx.send("```배팅금액이 보유 금액보다 많습니다.```")
        return
    choice = hole_dict[args[0]]
    await ctx.send("```게임 진행중입니다.....```")
    cpu = random.randint(0,1)
    await ctx.send(file=discord.File(img_list[cpu]))
    if cpu == choice:
        acc.updateMoney(str(ctx.author), int(args[1]))
        await ctx.send("```축하합니다. 승리하셨습니다.\n" + acc.currentDeposit(str(ctx.author)) +"```")
    else:
        acc.updateMoney(str(ctx.author), -int(args[1]))
        await ctx.send("```안타깝네요.. 패배하셨습니다.\n" + acc.currentDeposit(str(ctx.author)) +"```")
    
@bot.command(name='돈')
async def money(ctx, *args):
    if acc.search(str(ctx.author)) == []:
        acc.addUser(str(ctx.author))
        await ctx.send("```유저 생성 완료```")
        await ctx.send(acc.currentDeposit(str(ctx.author)))
    else:
        stringbuild = "```" + acc.currentDeposit(ctx.author) + "\n" + str(stock.getOwnStock(str(ctx.author)))+"```"
        await ctx.send(stringbuild)
@bot.command(name='구제')
async def imf(ctx):
    await ctx.send("```구제 금융 서비스 입니다.\n 보유 자산이 200 이하일 경우 지급 됩니다```")
    
    if acc.currentDepositI(str(ctx.author)) < 200:
        acc.updateMoney(str(ctx.author), 400)
    return
@bot.command(name='치트')
async def cheat(ctx, *args):
    if str(ctx.author) not in adminlist:
        return
    acc.console(str(args[0]))
@bot.command(name="상점")
async def shoplist(ctx, *args):
    if len(args) == 0:
        ctx.send("```1. Flag 5,000,000$ \n 2.Coffee 100,000$```")
    choice = int(args[0])
    namest = str(ctx.author)
    if choice == 1:
        if acc.currentDepositI(namest) >= 5000000:
            data = os.getenv("SECRET")
            await ctx.send(str(data))
            await ctx.send("SgOm에게 해당코드를 전달해주세요!")
        else:
            await ctx.send("계좌 잔액이 부족합니다." + acc.currentDeposit(namest))
    elif choice == 2:
        if acc.currentDepositI(namest) >= 100000:
            data = os.getenv("COFFEE")
            await ctx.send(str(data))
            await ctx.send("SgOm에게 해당코드를 전달해주세요!")
        else:
            await ctx.send("계좌 잔액이 부족합니다." + acc.currentDeposit(namest))
@bot.command(name='31')
async def beskinra(ctx, *args):
    if len(args) == 0:
        await ctx.send("```31게임 시작합니다\n1~3 까지 입력 가능합니다\n 봇상대로 승리시 100000000000$ 지급```")
        await ctx.send("2")
        sess[str(ctx.author)] = 2
        return
    clchoice = str(args[0])
    if str(ctx.author) in sess:
        if sess[str(ctx.author)] == 31:
            await ctx.send("패배")
        if sess[str(ctx.author)] > 31:
            await ctx.send("게임을 다시 시작해주세요")
            return
        if clchoice == "1":
            sess[str(ctx.author)] += 1
            await ctx.send("Now: " + str(sess[str(ctx.author)]))
            await ctx.send("Bot의 차례........")
            sess[str(ctx.author)] += 3
            if sess[str(ctx.author)] >= 31:
                await ctx.send("패배")
            time.sleep(1)
            await ctx.send("Now: " +str(sess[str(ctx.author)]))
        if clchoice == "2":
            sess[str(ctx.author)] += 2
            await ctx.send("Now: " + str(sess[str(ctx.author)]))
            await ctx.send("Bot의 차례........")
            sess[str(ctx.author)] += 2
            if sess[str(ctx.author)] >= 31:
                await ctx.send("패배")
            time.sleep(1)
            await ctx.send("Now: " + str(sess[str(ctx.author)]))
        if clchoice == "3":
            sess[str(ctx.author)] += 3
            await ctx.send("Now: " + str(sess[str(ctx.author)]))
            await ctx.send("Bot의 차례........")
            sess[str(ctx.author)] += 1
            if sess[str(ctx.author)] >= 31:
                await ctx.send("패배")
            time.sleep(1)
            await ctx.send("Now: " + str(sess[str(ctx.author)]))


bot.run(TOKEN)
