${SegmentFile}

${Segment.OnInit}
	System::Call kernel32::GetCurrentProcess()i.s
	System::Call kernel32::IsWow64Process(is,*i.r0)
	ReadRegStr $2 HKLM "Software\Microsoft\Windows NT\CurrentVersion" "CurrentBuild"
	
	${If} $2 < 10000 ;Windows 7/8
	${OrIf} $0 == 0 ;or 32-bit 10
		StrCpy $AppName "qBittorrent"
		${If} ${IsWin2000}
			StrCpy $1 2000
		${ElseIf} ${IsWinXP}
			StrCpy $1 XP
		${ElseIf} ${IsWin2003}
			StrCpy $1 2003
		${ElseIf} ${IsWinVista}
			StrCpy $1 Vista
		${ElseIf} ${IsWin2008}
			StrCpy $1 2008
		${ElseIf} ${IsWin7}
			StrCpy $1 7
		${ElseIf} ${IsWin2008R2}
			StrCpy $1 "2008 R2"
		${ElseIf} ${IsWin8}
			${If} $2 < 10000 ;Windows 7/8
				StrCpy $1 8
			${Else}
				StrCpy $1 "10 32-bit"
			${EndIf}
		${ElseIf} ${IsWin2012}
			StrCpy $1 2012
		${Else}
			StrCpy $1 "Pre-Win10"
		${EndIf}	
		StrCpy $0 "10 64-bit"
		MessageBox MB_OK|MB_ICONSTOP "$(LauncherIncompatibleMinOS)"
		Abort
	${EndIf}
!macroend

${SegmentPre}
	;Get the system's main TEMP and use that to ensure a second instance of qBittorrent doesn't occur
	ExpandEnvStrings $0 "%PortableApps.comTEMP%"
	${If} $0 != ""
		System::Call 'Kernel32::SetEnvironmentVariable(t, t) i("TEMP", "$0").r0'
		System::Call 'Kernel32::SetEnvironmentVariable(t, t) i("TMP", "$0").r0'
	${EndIf}

	${Registry::StrToHex} ":" $9 ;$9 now contains the ASCII code for :
	ExpandEnvStrings $0 "%PAL:Drive%"
	${Registry::StrToHex} $0 $1 ;$1 now contains the ASCII code for current drive
	${WordReplace} $1 $9 "" "+" $2
		
	ExpandEnvStrings $3 "%PAL:LastDrive%"
	${Registry::StrToHex} $3 $4 ;$4 now contains the ASCII code for last drive
	${WordReplace} $4 $9 "" "+" $5
	
	System::Call 'Kernel32::SetEnvironmentVariable(t, t) i("PAL:DriveHex", "$2").r0'
	System::Call 'Kernel32::SetEnvironmentVariable(t, t) i("PAL:LastDriveHex", "$5").r0'
!macroend

${SegmentPreExec}
	ReadINIStr $0 "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale"
	StrCmp $0 "ar" "" +2 ; Arabic
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ar_SA"
	StrCmp $0 "be" "" +2 ; Belarussian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "be_BY"
	StrCmp $0 "bg" "" +2 ; Bulgarian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "bg_BG"
	StrCmp $0 "ca" "" +2 ; Catalan
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ca_ES"
	StrCmp $0 "cs" "" +2 ; Czech
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "cs_CZ"	
	StrCmp $0 "da" "" +2 ; Danish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "da_DK"
	StrCmp $0 "de" "" +2 ; German
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "de_DE"
	StrCmp $0 "el" "" +2 ; Greek
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "el_GR"
	StrCmp $0 "es" "" +2 ; Spanish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "es_ES"
	StrCmp $0 "eu" "" +2 ; Basque
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "eu_ES"
	StrCmp $0 "fi" "" +2 ; Finnish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "fi_FI"
	StrCmp $0 "fr" "" +2 ; French
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "fr_FR"
	StrCmp $0 "gl" "" +2 ; Galician
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "gl_ES"
	StrCmp $0 "hr" "" +2 ; Croatian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "hr_HR"
	StrCmp $0 "hu" "" +2 ; Hungarian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "hu_HU"
	StrCmp $0 "hy" "" +2 ; Armenian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "hy_AM"
	StrCmp $0 "it" "" +2 ; Italian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "it_IT"
	StrCmp $0 "ja" "" +2 ; Japanese
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ja_JP"
	StrCmp $0 "ka" "" +2 ; Georgian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ka_GE"
	StrCmp $0 "ko" "" +2 ; Korean
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ko_KR"	
	StrCmp $0 "lt" "" +2 ; Lithuanian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "lt_LT"
	StrCmp $0 "nb" "" +2 ; Norwegian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "nb_NO"
	StrCmp $0 "nl" "" +2 ; Dutch
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "nl_NL"
	StrCmp $0 "pl" "" +2 ; Polish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "pl_PL"
	StrCmp $0 "pt" "" +2 ; Portuguese
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "pt_PT"
	StrCmp $0 "pt_BR" "" +2 ; Brazilian Portuguese
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "pt_BR"
	StrCmp $0 "ro" "" +2 ; Romanian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ro_MD"
	StrCmp $0 "ru" "" +2 ; Russian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "ru_RU"
	StrCmp $0 "sk" "" +2 ; Slovak
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "sk_SK"
	StrCmp $0 "sr_RS" "" +2 ; Serbian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "sr_CS"
	StrCmp $0 "sv" "" +2 ; Swedish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "sv_SE"
	StrCmp $0 "tr" "" +2 ; Turkish
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "tr_TR"
	StrCmp $0 "uk" "" +2 ; Ukrainian
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "uk_UA"
	StrCmp $0 "zh_CN" "" +2 ; Simplified Chinese
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "zh_CN"
	StrCmp $0 "zh_TW" "" +2 ; Traditional Chinese
		WriteINIStr "%PAL:DataDir%\qBittorrent\config\qBittorrent.ini" "Preferences" "General\Locale" "zh_TW"
!macroend