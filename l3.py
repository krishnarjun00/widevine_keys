# -*- coding: utf-8 -*-
# Module: KEYS-L3
# Created on: 11-10-2021
# Authors: -∞WKS∞-
# Version: 1.1.0

import base64, requests, sys, xmltodict
import headers
import cookies
import json
from cdm import cdm, deviceconfig
from base64 import b64encode
from getPSSH import get_pssh
from wvdecryptcustom import WvDecrypt

import logging
logging.basicConfig(level=logging.DEBUG)

MDP_URL = input('\nInput MPD URL: ')
# lic_url = input('License URL: ')
# hardcoded for kinopoisk.ru
lic_url = 'https://widevine-proxy.ott.yandex.ru/proxy'

# pssh = get_pssh(MDP_URL)
# pssh = 'AAAAZXBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAEUIARIQy8Z1jMAZRKm1xt0uRD4eRhoNd2lkZXZpbmVfdGVzdCIgNDMxNTA4MjQ4OWQ4NzY3N2IyMWY3YzgzNTkzZmNiNzM='
pssh = 'AAAAZXBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAEUIARIQy8Z1jMAZRKm1xt0uRD4eRhoNd2lkZXZpbmVfdGVzdCIgNDMxNTA4MjQ4OWQ4NzY3N2IyMWY3YzgzNTkzZmNiNzM='


# params from mdp_url:
# ottsession=5945048d6f844d1699054cc5d44548f1&
# puid=339572866&
# video_content_id=4315082489d87677b21f7c83593fcb73&

print(f'{chr(10)}PSSH obtained.\n{pssh}')

def WV_Function(pssh, lic_url, cert_b64=None):
	"""main func, emulates license request and then decrypt obtained license
	fileds that changes every new request is signature, expirationTimestamp, watchSessionId, puid, and rawLicenseRequestBase64 """
	wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)                   
	widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers.headers)
	widevine_license = requests.post(url=lic_url, headers=headers.headers, 
		json={
		# "rawLicenseRequestBase64": str(b64encode(wvdecrypt.get_challenge())), 
		"rawLicenseRequestBase64": "CAES8h8SXQpbCkUIARIQy8Z1jMAZRKm1xt0uRD4eRhoNd2lkZXZpbmVfdGVzdCIgNDMxNTA4MjQ4OWQ4NzY3N2IyMWY3YzgzNTkzZmNiNzMQARoQKMPoWROeD3SRLBHOALur9hgBIJD_uI0GMBU4qqyWtgFCgB8KFGxpY2Vuc2Uud2lkZXZpbmUuY29tEhAXBbkXzBIEhosGMzovdyqMGsAcTTL1N_QjRX_1tXrGyxbUyC2eOarUcKa1hJQyaAs5VIRvG1RWI-V3ozi1yd9WkbtD18rqb2vDQAojrlZXS5TTGeZtqO0_Wrp03Qex-Yl5GO_cO6zOP2GvOUhFgzN3t0PY4vS790k5c823zJrsxsr7IxQNEKvN_gXf4eJrgItWqeE22_TxHLbW16OvmS8bu5cu7hgjn2WFz-DAj9srI1Zu8HLcWOn4OA1RRoZroLbP4Mle2Vxp0yvvfuzmGNIDlrSz0PP0_wSKyAKtWci-cVqfQXLabINiy01h7exhPZqtjMA2NFFhf6eyaFWkFXB7NWOiq04PEEZXEMdl9fwSZCgxzwdr2xpFBM7uLMBU8XTpY9hActHUqKwtKw8B1tv9aDMWKoXCwHQWBdScENnZn4qxxObovESZGCfu-CxD5Kgq59t0wvwnkHqXksSQlOCFuFOzslIjXbm8Dmt0Iptr0Qbfd6Bnyk5-rb6Yi_VJNV3_zU_DvUFYPFklcqPwDoUa4QuAS8rZVG8ypLeSvQ1-UOyfXfKpUTSqX5qVGj6Niaz1FBAJbhA_BrTkr4shW2WGtS1VvDETi9Q6e4Ah4t9ONpJ_az6VwiMfvPCzSXt5nWdY-NOmMdBH-LoYknkIw4FlOEYtuXrmzUs_Xj6apeYIWaNof7Euzo4jDYBxpVBaoTa6due6Ske9GymiAK8yEtsuXhtJjf2qxB1O5GLPWLCG_bxzDfvoRG0Ha07M-lTKSi9oVM-natDonhI1Khz1b6nhUUtAz5T8W6UPDF3pUEETa35IOeFQzdESSXAGdP41Ug8CiaSv1CGo91NmvNT5AqRyMs9Z9BOqeO7qBCNwDsX_L8Me3i7k6R1LwIvOIC6yabhJg18y7Quok4kiBM96qkKcDIzUxiE3A_RkX9ACCozVx6d1J2j6rMLn6WSgs5ccDUNIR1nDCFDBjay_i_so-NwG2tZgvMTmi41n-Wj5d44VhSs3HiX4WMVPa1Ir9zCqekmJETg9uDIdaCbihENlLblmP3V24C710eaYcJBd6V1PGueTlyO4_gf-f4IqxoTez8Rbxgz2sxhUYtJeVpukP63tFmekw15Zu-Goix5kdRSD4GsRDBQ26OewAM2WQH80yKRB-62ZE0FOr7HC0Mi0bXHo8C3QHbb0BJ5VdTq9kbicOkBA474VNH47IxfrUMjsye9YJjwd6BMZs55_E5W5Ru8uLDXU5y81x6vr9VoT8nXlRglPc4Lff5lJuQaYql8-OGRC_cFA4DpHgfNOM916JbD-XbxZo-cOiTSe6w3KnYWqNuhI6ZSKHTDaEnapEyhOL4L99lDrmDdjD5qDXGDabpP9bokROrgQ7z-iLlO0oHCv3UROQFja9M_rplTPbbqo9hvGU88UmV4yNm1zU9v_ncYG0apjyCEGSEd-CrqHlDwaeg6yb0JGr9UoGyE0CTWS_vxI8AxgIgSCHXKGB6ImzNnC0oksvYz9iPWzs85_ZyHDWrKg8d7p0gXuZT4FjXJkLzctynm-3aY3lcfU4NmkUDBKwDeIoc3lm-klvdB3LWeRMEk_1bOdiYQJgfi7AqBOT68btgiF11FPITeZ27hPiAY2EHL6sh2EeAYpcwECQQs0UnSwpuiGkNmcCfSMhnJEXtv2Sf0fCUMvFEI6faSZ2LRYkis7KLvtfrweHgWxLUUzXIKu2G9MDCFDaByg4TadUH8W_yQk-cmtJdUbz4qnSW93WX1uSABqAL2DOkH7BMm8f8DkZ4SZgPBVTvg82h_RM3YRAig9djnyJtSf1zuVL1ag7JBPjPvuquNcU6qYTKnRVU-T4ZK6rGjD2HDG-bpXkzzBKBkYMQWELjWoAdLFf_-Rmlw4tuAi06gFojhYXA4e535XdYKYdofgf7i9H0xWJvPj0boDYeSYNO5PzdxR3ma05O_cfBTDjRrFGaI6KNUU0ALrG7mdn0w_YQSxQVIbwlJ0Fdb1B1j8yp1uBX9PdxyX_Y4UBn9aKAZkJ3d9Njtik_Q3O_71gU_lCqY3VZb23cJmgPPAx_T4WcEpG3gXEB2HcON8gS6dfdqAB373_ZiafDDaAzzzymL5oeqedCeG_a2krp1KbQGXnuUYYyzYeH2cXci-o1Nq6GyE5qeVR9KBewXkEetyEVZlBrucacCBgZMo8mc_g4lC7BMgD69B50eaukeo7EU015C79ScK77tM7gi0nnp2OXHFjr3XKnH0kzQR_y2Hy2yNjjxLqlvenP8hvsm04kX0_qhi-9xoSOmI4xtyb8kJ15ed-o0aT2LZ40rLM7DcpOhxvmpA4Rvm1_vRW_JpBp4jjkDOn37S5Y01Z23WjVDbCOetp3SRq1Bgj-uo6YzgqcR1rNYZ7suGuqCICY0NmGO9NBXkAAV0RLNyk3DCJB9lES3roa2YFrQv9tHx69kD4Kwxvnj2Fl_StZc24pxkuFUOS2SCcRLRggQ3-AKPDUUYC5CxqHSMr1Tfojn7TQS6m_oFHOd3LfO9ZtWK0GnwsBXFT6_n3ArARN6Rq71YYSSZDaP4Fj9oT8oWOn9FOC1EwiZ361mBpVxlTjNv8lwO6ErJZmmg7To6hKmMwB1s5kZ69L5Y46cLSbrS-tQav0luXga4tygDwt1BRjbgSPJ9jLRo8h85DFEl9ZfwGtBbPDh6fMPJnBkASezmfz8pb-d2ZLVMyaJU6pjhKctY5DeI_C2KmwNKhmTbN4Orhnq3v8F7Uu90si1g30_m0XQ4t1cA82xMMoBGAyrHQs_8mi_jZ828ghsIDtd4Hg1Bmz33SpugvbbOp5I7CDG_QyTNJV1dACMK7TZa-TS48CJchT2dL2EH0rkgJSL2V3CdcMq9ZoPaBr7z3vLjxOPs4ThiUF2hvb46wXRhq_37nB3oGsIEEQnauDA03N1O4Q_xJA71GmXybU27UuKE1ytE0lqkUM703pwPwuiKQ_Uv7YYCauhljpDRd1vJDTX7_DJZd_rb2e_w1g_XqkXbL9UID6rlzbg_hjhn7T6SCvFc8Y-j8koS4Lc6V3cVWcMo-uBKjEb4WWaeW06Xpb0j7fUlJWdWdEjPB8qKwtcHAwVpLdFH3G3W2xABQO6H5rt_vM5JICZZEC8SImNiZozJ3xQnL9D_9hsXHB8XjpLaL7R3N7Vl2j0z04V1COegDwq1nD2B3unFfEOqHQW1k9-SxN78WIvwgZ65ELPFL32f-nNFHNDypg5HQq3I_PF4g2X9aWkw-H5MVskHqAm7vUUkZtwBBlSyynLo2PGdH4RurtualrH1JEJTCAGq2DaSp6fB15vlfsMTuH5Vg3pDUGFzY_Ym83XFNtNwk3T90OgMcZxFUdaFgYhUzdNYy5JkdMlnYkKsO-jwR_lOq-0cqP20p18all7e1gca-tJsxfCfakkLpo04SoXWMhdV9yOfb23Uwg7G8dXgS7w_SrlTbqozOl7FZ3GuZsnTuttFknWT6jlw4Ew3-SNWUji9U8263KA8cTPIHKLf-lIN-uy2lTkUBW5yMhe9wYqV3fxF_MoSK02gEmXZoIeHrxal1l5pjC-S3jeMifE2MMLTD75TVw7a-Df-vK-vmXx2t_twYiq7-p7LRqkJEZyRusArIuIGPF3ogySNkB6Ktjc-wvr_7YEI7kIHUBeM7Gb0ftTI9YCuUy3U7wUbCySF2xL9BDyFgKMa9dbBqpL7A_tYmX17mAcxVH6IQXthDy4Q-KFR62JlzXThYfpWZChFYJX79zTBVi5plP_4epg7uCF5rE0l1fGIpQ06xGfI2791W02kTfVx8c5OvqvogP7Gl1Imq08niUbElvpHeeMkAxKEKVDIdHXk5ASXH1sIh1IvhZLoQWhlsyK_uljyeAnGeNPnvoDaa8eEmQcwdXYHA5f5iBea77Qk4LH1XmyIGaoaWUA-1LEr1spKk_w4lc54WfvDpysBSHvO4pA-pyL0zs1cu7zS1LDqYoKdQx_X_uikUJw14pApGrXpqI4zwAj6PRcoUeDTMAvHkv1t3QZ_Nt9kNMBL4owRVhI6k2Et0gMISrkm1RSWDsCuFo2pPHWY5vBAAlE68bSPPms8MYHtdGi7CYwow2q3URBlEFBdfikl3oI5nqxu0Tpq_1R4-HEfX1tvC3z-mxaaWGC5mHr7ozQT5JEssSOlNfI9jX6d-od8N_GR82_0y-qaj1P2xjeK-txZZ25tBqxb7h6SSEP4W_TDp0ts6k0QKjzy31YYfhyvC9ls0lxhADoPmcRvYpentRPRJmw0dQdz-zf4EUApAfgzTizbIEI3p7i-8aCncJuVEoLD3EFNQ5nOJqvSO0sA1M5A8hj2QfgGZIK3DE5nRsvw03IuTl_5ps8bfKIt6HdZWYjeYT4pLNw9oqyC5hK4uUC37eiYYid0Tr7XmLYr7PzFm9mNn1UO90mUC-mDxeblJ8v1-SH22lyHW1Q2vwmLfnJJDMsnf0SyZu8kNcGjBcCSYH3Ps1KLBAGzi05PPbCgMIBHODeJ9j_3lG5tgXoOzo45Bpgz2vLCFjlPz7u7EJuphulZJJiCy6swo5dVLJvGQKrpJxQysyHrYQH1P5gRK0xr4dN7pvIAhRa_blrRzG5IaDsr2_UhG1QrGNKrfdpJct0mL0PHhvDGkYuqWMmfTQRoZHFCYbse1D4tsCThma3cPGPc-U4V7Kx-tZ8a_W1zVDkq5OfSgl-et90EllP2NdS3jcVoTZUGn27rtRBVJG0Um6FvWZAUhadEQb524iMPJVQIFCfMQbYm8VS7uV__f4EyFD9Q7lrqM3RNIIhPAXhT1Dk0CoRE1Qk6_3JfMIWIg24Z3l_4lJEN_XcCOVu9QQXbrw4GcvAKYI6-Mn8WB78uRSJ2m5IQ7m25r3my-X3RZpAjcVuZXqxAa6w-4WLdIhDxT_iZIcdCcvjTBnKpufXRKoACNGcWVV1m3rRIgp1e2civ8_pdGLNUQmDa7yoyj_w9-CGGuWOWjxvGJK7Mj-FfBJBDfqEtKmFUAacXCi_n0PMA4_CQLvhRmR4jx2XAR-LXjSB2vlXA0xTE-087xsUnINfxxWY_Y8XtGc0uC35YCA1jX7AtQEO0k666TVTMHlxrpyhb-gaASJveAqAjy7NwJyWeqCCWueQhhRE4CX10OPrESnR_GTl9Guv4E_8CQWd9gM57kqYcwHiC60qAaxC22Fvz8UZqOhbek1x-ME5Ldf41WqyPSpM7a8hkEyhM80FScULlAyFa9wJKTz74Q7OCAuRgCAxsyCrmFWdTUPbt3Ft2MhqAASgiHmjyCxxLsspXMj7wMtkz6O5d4ffJxIAsH1gwsIgWA4w9Wy5ypTz5H4ol0wWxec95EpLL7UghBC6Gscma_-p4HTuAsr3m4WkB7r_6aU_OvWQh7cQhc8i8DzE6jde8dH34CDYb0wSW3gbExUl1HajE5CUAOUG5J6pQPqFJNhPSShQAAAABAAAAFAAFABAWxZYqUuFFWA==",
		"puid":'339572866',
		"watchSessionId":"5945048d6f844d1699054cc5d44548f1",
		"contentId":"4315082489d87677b21f7c83593fcb73",
		"contentTypeId":'21',
		"serviceName":"ott-kp",
		"productId":'2',
		"monetizationModel":"SVOD",
		"expirationTimestamp":'1638831085',
		"verificationRequired":"true",
		# "signature": cdm.hash_object, 
		"signature":"b6ca3161c8bd38105e87770458aee16191214cfa",
		"version":"V4"

		})
   
	print(f'{chr(10)}widevine_license: {widevine_license.content}{chr(10)}')
  
	license_b64 = b64encode(widevine_license.content)
	# license_b64 = json.loads(widevine_license.content.decode())['license']
	wvdecrypt.update_license(license_b64)
	Correct, keyswvdecrypt = wvdecrypt.start_process()
	if Correct:
		return Correct, keyswvdecrypt   
correct, keys = WV_Function(pssh, lic_url)

print()
for key in keys:
	print('--key ' + key)
