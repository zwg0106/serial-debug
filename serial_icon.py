# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QByteArray

class SerialIcon(object):
    __base64Icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAFiAAABYgFfJ9BTAAAAGXRFWHRTb2Z0d2FyZQB3d3c' \
                   b'uaW5rc2NhcGUub3Jnm+48GgAADblJREFUeJzNm2l0VVWWx3/3vikhE5mBAK2QoBClMSA4VVXXkta2Fs3qssGytcpyAKKiuBRKpS' \
                   b'lE0CotC7tEq22hG1liiSU4EEBxYkgiqIBQTEkgBCKBQIb38qbkTffe0x9CXvKSN92XpNv/p3vP2Xufff73DPsMVxJCMJhYsB2LX' \
                   b'6VEg+slwVQNRkswHMgHkgEf4ETCicCG4KQEJzSZatnPntW3c2Ew/ZMGg4C5HzNeVrlPyPwYwTWAuR/maoBtquB/1s7kxAC5GMSA' \
                   b'EbBgOxavyiw0SpH40YAY7QUBFZLEmkAqH6z7B7wDYbPfBNy3mySjm6ckwQIgayCcigM2IfFqmoeX/mM2nv4Y6hcBD27hnzSZPyM' \
                   b'Y2x8n+oF6SeLx1TPYnKiBhAiYu52RksIrwL8mWvCAQvCZLPPoGzOo1auqm4B5ZUxH5kMgTW9hgwwXcNeaf2abHiVZj3DpFmYj8z' \
                   b'E/vMpDp09lpVtYqEcp7hZQupVSAa+jk7T/J6yVLvDQ6nkEYgnGVZnSrSwR8Ea88j8APCCGs3H58tj+RhWQQJq3jVcEPD9wvv2f4' \
                   b'V/Ol/BKLKGoXaB0C88KiWUD5ZHma8dz9jh+WyNqhxPN48R69gRIBozJqZgzcsme+FNSL584UEUiCRatnsnLkfMjEDD3YyZLGt8A' \
                   b'xv65IGivO4i7Zi++pjMgtJBcW5sNVVVD0owmM+mjrmDkz0oxpWT2r3gQQuKO/57B++EywxKwYDsWr8J3QHF/SvY2nsS+bwt+6zk' \
                   b'ALBYzkyddwdVXFZKdlU52VgYpGTl4OjpwutwcPHiMTR9ux+FwAyDLBnImXM/IW+cgGU2JOyLhUDUmrJ1JY5+scASUbuElIfGbhA' \
                   b'sUAvv+rTiP7gSgYEQuv/q327hh2tWYzaEVOd/q6+UrtLXZWPXqOr47dBwAS0oa4+5ehjlzeMIuIfhozUxu753ch4B5ZdyATCUJj' \
                   b'vhawId111t4GqqwWMzMvXcmt91yAwZDeHO9CeiJixca+c3TL+JwuDEYTYyZ+QjpRVMScasTErevmcFHIUk9CShZ584dmiIfK0we' \
                   b'kpdQAUKj+bPVeM+fIDs7g2f/fQ5FY0dFVYlGAICqBHh68QucqK1HlmWuuGspQwrGJeTeKU+HXUhi/K7ZKRe70kI+i2ZW3z7scue' \
                   b'5FCWhAtq+2Yz3/Alyc4by6ktPxKx8PDAYTaz841LGXzkWTdOo3fgHlHaHbjsuReGwyz3U7lff6pkeJEDadC75gs8/XRWC/U4nep' \
                   b'dIHfWHcVVVYDabWLZ4DtnZGbqdjASBxO+ff5K0tBQUv5e6v/5Opz7sdzpRhaDR55te9I4tvSsvSECRN/VFn6YZAFoDAU52dMRfg' \
                   b'KZi378VgAfn/JzCsSN1ORgPDEYTf1q5BAB363mcJ/fHrXuyo4PWQGdU7NM02SLk17ryggS0K+oveyodcblo9EXvn11w1+xBcbZy' \
                   b'2ejh3PaP14eV8Xr9rHt7G48ufJkPt+zuk1+25XOeWLiC9W+/j9cbvty8/GHcdGMJAA071sflW6PPxxGXKyTNEVBmdT3LAIVvtU5' \
                   b'uV5WQ3RwBfONw0BaIuZ7AdbwCgHt/NQNJksLKfLFzH+998CW1dQ2seXMzx6vPBPOqq2tZ++ZfOVVXz/sffMKOnXsiljX/oV8D4H' \
                   b'XaaG+oiupXWyDANw5Hn+7sUtUhN73rvgMuEWCUDWHDXUUIKu122ntFaj0RaLuA4mwlPS2FqZPHR5TbWX4g5L26pgcBNXUheeXlX' \
                   b'0e0k5KaRkFBPgCtB7+IKNeuqlTa7SgRIl2Hqs6HSwS4FGV6JENeTWOHzYY9wszg+f4YANOuLUaWw8/1DqebU6fPhaSNubygx3Po' \
                   b'bFF3+nscztBm2xO/mPUzAFxnq8Pm2xWFHTYbXk0Lmw9gCwSmAMg/es81rl3VkiNK0knCLpuNZr+/T56vpR6ASROLwup6PD5Wrtp' \
                   b'AIBBKYFFhd6XHFl4WkhcIKKxatRaPJ/zG78SJEzrL7nABoZVs9vvZFaPyAO2qOmTSek+B0RFQbokq2eWUEFTY7ZSkpTEmuZsvtc' \
                   b'MJQE720O40VWPvt0c5cLCaA4eqsVpD5+3rri0mLXVI8D0tNYWp105i3/6/BdMOfHeEhx9ZQsk1V1FScjXXTSsJRpOpKd26PlsTl' \
                   b'qzOEPm0x8NBlwstzk0eg6zcZfQL6bq4pAFNCA44nTT6fExJTydJllE9nU01KzM4tbJk+Rv87cjJsDbS01J47OFf9Emf//CvqV5w' \
                   b'CpfLHUyzWtv44stKvviykr+fOIHnViwCwGTuPmfxtpxFDM0P+qUHCtqtsldVrtalRefU8qnVSoPXg3aJgC7OW632iJVPTrKw6LG' \
                   b'7yexBVhcyMzN4/LE5JCVZwuoePlJFq7WtT3pLSwOfWq26Kw/QrmljZRVydWsCfk1jf0sTQuucIc7Ud640s7MyKBjR12Tx+DG8vu' \
                   b'pJpk6ZENHmlCkTeXXVCiaM7zueFIwYRnZWZzdzOp3B9CZrE/4Y/T0SApqWYVQFqQlpA2Zfd3M9U9/IT266BkmSWPHbeWzeVo7L1' \
                   b'cG4wtEUFY7iqgljIsYIPTEsP5cXfv80VVW11J46w6lT9aSlpTBjxvSg/vnzwbUMxg7964IuqIgkoypIStSAydcefD5efTr4XDAi' \
                   b'l/nzZoVTCYHT1c7Fi20MGxbaYiRJorh4HMXF4Vd93+7rHiwN3sjTZSwENGGWFU1NeKvF1KMFHD1ex7sbP49bd91ftvHLB56l9KG' \
                   b'nWbL0j3Hr1Z2q46Oy7gBI9sW/ZukNRWgGWZKlhA8HzV53yPv6d7ezY3fsRUqr1c6mD3fi9wcQQnD0aDV1p7+PqWezWln45AshaZ' \
                   b'K/P2ejkpCTJKlvdBMnenYBACEEK1dtYP2G7UTbbT5efQat18BVWbkvalk11Se4f+5TffQIJOw+RklWZLNsdMYWDY/eBEAnCRs2f' \
                   b'saKF9/sE/31EIonCejcIywr+4QnF/+hb+UBoSa2eQNglPHIRklYEzXQcxboja+/Pcprb2xK1HQQ5eV7WLsu7I420Em4yRvZj2gw' \
                   b'ILlkI/L5RJ0L1wJ64vMd31K2rSJR8zSeO8fKP62NKWdxNCVkX5Jok2WDdDq2aHiYvNEJAFizbjMXLrbqNy40FjzxXFyiZlcC9oE' \
                   b'kyVAtgxR9VyECJE3FGIg9AquqxgYd02MXysv34vfH3owBMLsT68WpslwhZ5vNZXIcEVpvxGr+PbGz/IC+ViA0Xnv97fh9abfHb/' \
                   b'sSJCDPaN4ml89OOpNlMvVdZcSAWQcBqqqxu+Jg3PJ1dWfi/voAhg79E1mawejefmdSvdz5YijTa8AUZQYIh8PH4r++s/fr+MkCM' \
                   b'CQwCyQb5Ero2hUOaMv1dgI9XQCgqqYeRYm8t9gFCfj0c30zh+TTHw1qqvpbuETAoXuH1qcbjRejq4SidxgcC35/gNq6hphygYAP' \
                   b'l0sfuVJA353JDJOxufa+nIPQ41zAIkvv6TGitwUAVJ+ojylz8UKzbrso8Y8XAKkGOXioECSg1SstM8ly7DZ6CXrHAIATJy8teML' \
                   b'MOl1Jx6vC7yZFg6YqEOdhnlGSNcmpLO96DxJgm5fpGGG2fBZvoYm1gE4Criga3Wdz5Lpp1wBQXhF9URQJZpctLrnhFvNXxx7ODX' \
                   b'69kOsvfofrHu85U7PiEzHvBhh19lOA5hYbZxsuMnrUMGbcdiMff7oXgKLCy7nyykKEpnKsSvdlz04cb8Kdnh1VxGSRNDnbOxu6D' \
                   b'25DCKieX2DNfaH1/dZ69Y5Y5ZnVxBYgmz7aycIFdzF/3ixm//xmqk41UVR0OQAVFZFPhGL647KiGqLLZOca3jm8KDtkkOnzpVsX' \
                   b'59yZnCVF/bxG4cMgEluG7ir/jnPnO33Iy80MVl5oKn/+r78kZBMgKRC9CyRnSe1Ni7Pv6Z3ehwABIm0oN8pR7oZZNP3NvwuKqvL' \
                   b'4U69Qufcw7nYPkgROh4OH5i/B50t8c8OkRA6HZRNkZnFruLyI1+Tyfmdd23JWuT9cXpb/LNe2vZOIn30Q7ppcIgikj+HoqEfC5u' \
                   b'WNNr7VtCT73nB5EQe75iXZD2SNMISNXMz9aAGDBaMS3qecEabTkSoPMW6C2ZblXJaeL/dZa1q0xAbAwYSs9g2H0/Pl1pZlWVF/5' \
                   b'ohKgADNWZObn5IjhYww/RkDBguSGno0lpIj2525jph3dWLO92Ijars5b/iQTIIk/BC7gNC6w+GUTKm5vTU3TzxaGPPAMK7LkGIZ' \
                   b'/o7k/NzMAvkwElgSjAEGE0LTkAmQPdJwyP1iXr5YHftfAdBxG1QsQ7M9kzvpskLzanP/ftQaFEiSzJgC+9bWpTklevR0X4c9syj' \
                   b'zQXfxT+9uThuf2JHsIECk5gml5Pb7a5+5aqZe3YR/m5M2YSj6unJPfsPuaSmBhI8W+hUHyEYL7jE3H675u7tLxDIS+iD9/nFywp' \
                   b'LK4RZ706HsC/vzjZr+SwqJECBJMmr+BJdy5eTio8/fEnuXJZqtgfp1duryr8Z02NyfpDTVjMv01se9w6aHAClpKP784oakoVk37' \
                   b'vvPO/tV8aDNwfh5uviZ/QtMLfXLMqxVWcn+6BvOsQiQTRaUnCK3Z/TUl2pevjm+kxIdGBQCeuLHyyun2p2B56R265SkjpZ0Q6DD' \
                   b'YFQ9klH1YtR82Nta0DSBJBvAYEKYhmjqkBwv6cOqU9LMS7967Z7tg+nf/wKBc9sC1/vWcQAAAABJRU5ErkJggg=='

    def getQIcon(self):
        _pixmap = QPixmap()
        _pixmap.loadFromData(QByteArray.fromBase64(self.__base64Icon))
        _icon = QIcon(_pixmap)
        return _icon