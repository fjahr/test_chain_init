# Bitcoin TestChainInit 

This project includes tools to embed interesting scripts and transactions into a new bitcoin testnet chain. When such transactions are embedded in a chain early and are then protected by a checkpoint, this forces all software that interacts with such a chain to parse and validate these transactions. This means it is a test vector that is very easy to implement for any project.

The project should make it easy to repeat this exercise for the launch overy new test chain in the bitcoin network.

The project seeks to utilize the functional test framework of Bitcoin Core where ever possible and follows ideas of projects like the [Optech Taproot Workshop](https://github.com/bitcoinops/taproot-workshop). This should make it easier to maintain the project and it also means anyone who has contributed to the functional test framework previously should also be in the position to contribute here.

## Ideas for data sources

- [ ] Testnet 3 blocks up until height 546
- [ ] [Bitcoin Core Fuzzing Seed Corpus](https://github.com/bitcoin-core/qa-assets)
- [ ] [Taproot Functional Tests](https://github.com/bitcoin/bitcoin/blob/master/test/functional/feature_taproot.py)
    - Note the `--dumptests` feature
- [ ] [Weird Bitcoin Transaction](https://stacker.news/items/600187)
    - [Source code](https://github.com/vostrnad/bitcoin-easter-egg-tx)
- [ ] Old bug exploits and policy violations
    - btcd crash transaction (2x)
- [ ] Test data in core
    - [Valid txs](https://github.com/bitcoin/bitcoin/blob/master/src/test/data/tx_valid.json)
    - [Invalid txs](https://github.com/bitcoin/bitcoin/blob/master/src/test/data/tx_invalid.json)
    - [Scripts](https://github.com/bitcoin/bitcoin/blob/master/src/test/data/script_tests.json)

## Discussion

<details><summary>bitcoin-core-dev IRC 2024-05-30 (<a href="https://bitcoin-irc.chaincode.com/bitcoin-core-dev/2024-05-30#1030087;">link</a>)</summary>

```
14:15 <fjahr> #topic script/chain replayor
14:15 <fjahr> I am working on the Testnet4 PR and it has been expressed that it may be interesting to have some edge cases in the chain that are in Testnet3 and maybe also from tests/fuzzing
14:16 <fjahr> My question is if there are any projects known that could help replay scripts/blocks etc. ? I didn’t find anything that could help automate this but maybe people have some creative ideas
14:17 <cfields> hi
14:17 <gmaxwell> fjahr: one could instrument the code to dump scriptpubkey/scriptsig pairs while validating, in a friendly form. Then some work with grep to remove the boring common stuff?
14:18 <gmaxwell> at least to the extent that interesting stuff is pure script only. though presumably there are other things like creating and spending 0 value outputs, weird locktime/seq stuff or whatever.
14:19 <sipa> fjahr: can you even replay, unless coinbases are copied? or do you mean recreate them (new signatures etc)?
14:19 <fjahr> gmaxwell: yeah, that sounds like a good approach for some of these.
14:19 <gmaxwell> I think andytoshi at some point long ago had some script symbolic execution stuff that could generate signatures in a script template.
14:19 <gmaxwell> but there may be a number of interesting cases that just don't have any checksigs in them.
14:20 <fjahr> sipa: I was thinking that if I fund the coinbase addresses that are used in testnet3 in testnet4 first, I should be able to replay transactions in order but I haven't looked into it deeply yet
14:21 <sipa> fjahr: that does not work, the txids will differ
14:21 <sipa> and the txids contribute to the sighashes
14:21 <gmaxwell> you could copy over the entire blocks however, and replay stuff.
14:21 <gmaxwell> though that's a pain.
14:21 <sipa> yes, that works, but you cannot miss anything
14:22 <sipa> well, you can strip things, but for a transaction to be replayable, its entire tx dependency graph, down to all coinbase transactions it directly or indirectly uses funds from, must be replayed too
14:22 <fjahr> yeah, the txs will need to be adapted but they could use the same scripts
14:23 <gmaxwell> yes to reuse scripts you'd need to have code to resign for any checksigs. not necessarily trivial depending on what crazy things are in there.
14:23 <sipa> probably doable by hand if we're talking about a few dozen interesting scripts perhaps
14:23 <sipa> but if we're table about more, you'll want some kind of automation
14:23 <sipa> *able
14:23 <gmaxwell> yeah, first step would just be to extract and grep out the standard types.
14:23 <sipa> *talking
14:24 <gmaxwell> and ones that have no checksig are also trivial to replay.
14:24 <gmaxwell> but if there is stuff that is using OP_SIZE on data that also goes into checksig, gooood luck. :P
14:24 <gmaxwell> (I know I had constructed such things, but I don't recall if any of those went into testnet3)
14:26 <fjahr> Ok, too bad nobody has solved this problem already :p If someone has more ideas or wants to work on this, let me know. I will also open an issue for this topic.
14:27 <fjahr> Anything else to discuss?
14:27 <fanquake> 27.1rc1 is tagged and binaries being built. Please build & test etc. Report any regressions / issues
14:28 <sipa> great
14:29 <fjahr> #endmeeting
```
</details>
