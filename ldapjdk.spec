%global spname		ldapsp
%global filtname	ldapfilt
%global beansname	ldapbeans

Name:		ldapjdk
Version:	4.19
Release:	5%{?dist}
Epoch:		0
Summary: 	The Mozilla LDAP Java SDK
License:	MPLv1.1 or GPLv2+ or LGPLv2+
Group:		Development/Java
URL:		http://www-archive.mozilla.org/directory/javasdk.html
# hg archive -p ldapjdk-4.19 -r default -t tgz -I buildjsdk.txt -I java-sdk ldapjdk-4.19.tar.gz
Source:		http://pki.fedoraproject.org/pki/sources/%{name}/%{version}/%{name}-%{version}.tar.gz
# originally taken from http://mirrors.ibiblio.org/pub/mirrors/maven2/ldapsdk/ldapsdk/4.1/ldapsdk-4.1.pom
# changed: gId, aId and version
Source1:	http://pki.fedoraproject.org/pki/sources/%{name}/%{version}/%{name}-%{version}.pom

#######################
## ldapjdk-4.19-4
#######################
Patch0:           ldapjdk-Added-getter-methods-for-JDAPFilter-classes.patch
Patch1:           ldapjdk-Added-gitignore-file.patch

Requires:	jpackage-utils >= 0:1.5
Requires:       jss
BuildRequires:  ant
BuildRequires:  java-devel
%if 0%{?rhel}
BuildRequires:	jpackage-utils >= 0:1.5
%else
BuildRequires:  javapackages-local
%endif
BuildRequires:  jss

Provides:	jndi-ldap = 1.3.0
BuildArch:	noarch

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%package javadoc
Group:          Development/Documentation
Summary:        Javadoc for %{name}
Obsoletes:      openjmx-javadoc

%description javadoc
Javadoc for %{name}

%prep
%setup -q
# Remove all bundled jars, we must build against build-system jars
rm -f ./java-sdk/ldapjdk/lib/{jss32_stub,jsse,jnet,jaas,jndi}.jar
%patch0 -p1
%patch1 -p1

%build
# cleanup CVS dirs
rm -fr $(find . -name CVS -type d)
# Link to build-system BRs
pwd
%if 0%{?rhel}
( cd  java-sdk/ldapjdk/lib && build-jar-repository -s -p . jss4 jsse jaas jndi )
%else
( cd  java-sdk/ldapjdk/lib && build-jar-repository -s -p . jss4 )
ln -s /usr/lib/jvm-exports/java/{jsse,jaas,jndi}.jar java-sdk/ldapjdk/lib
%endif
cd java-sdk
if [ ! -e "$JAVA_HOME" ] ; then export JAVA_HOME="%{_jvmdir}/java" ; fi
sh -x ant dist

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar $RPM_BUILD_ROOT%{_javadir}/%{spname}.jar
install -m 644 java-sdk/dist/packages/%{filtname}.jar $RPM_BUILD_ROOT%{_javadir}/%{filtname}.jar
install -m 644 java-sdk/dist/packages/%{beansname}.jar $RPM_BUILD_ROOT%{_javadir}/%{beansname}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}-1.3.0

pushd $RPM_BUILD_ROOT%{_javadir}-1.3.0
	ln -fs ../java/*%{spname}.jar jndi-ldap.jar
popd

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "ldapsdk:ldapsdk"

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r java-sdk/dist/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files -f .mfiles
%defattr(-,root,root,-)
%{_javadir}/%{name}*.jar
%{_javadir}/%{spname}*.jar
%{_javadir}/%{filtname}*.jar
%{_javadir}/%{beansname}*.jar
%{_javadir}-1.3.0/*.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,)
%dir %{_javadocdir}/%{name}
%{_javadocdir}/%{name}/*

%changelog
* Thu Oct 12 2017 Matthew Harmsen <mharmsen@redhat.com> 0:4.19-5
- Fix build for CentOS 7 (mharmsen)
- Resolves rhbz#1465103 - Missing getter methods in JDAPFilter classes
  (edewata)

* Wed Oct 11 2017 Matthew Harmsen <mharmsen@redhat.com> 0:4.19-4
- Mozilla Bug #1376300 - Missing getter methods in JDAPFilter classes

* Wed Sep  6 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.19-3
- Don't rely on build-jar-repository for locating JVM extension JARs

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar  8 2017 Matthew Harmsen <mharmsen@redhat.com> 0:4.19-1
- Resolves: rhbz #1394372 - Rebase ldapjdk to 4.19 in RHEL-7.4

* Mon Oct 31 2016 Matthew Harmsen <mharmsen@redhat.com> 0:4.18-16
- Resolves: rhbz #1388500 - ldapjdk fails to parse ldap url with no host:port
  (mreynolds)

* Tue Aug  9 2016 Matthew Harmsen <mharmsen@redhat.com> 0:4.18-15
- Resolves: rhbz #1353564 - ldapjdk needs to support IPv6 (mreynolds)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 04.18-14
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Matthew Harmsen <mharmsen@redhat.com> 0:4.18-12
- Appended full URLs in front of source files

* Sat Aug 18 2012 gil cattaneo <puntogil@libero.it> 0:4.18-11
- Added maven pom

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 31 2011 Rich Megginson <rmeggins@redhat.com> 0:4.18-8
- Resolves: bug 684012 - LDAPSchemaElement.getOptionalValues() mangles values
- upstream bug https://bugzilla.mozilla.org/show_bug.cgi?id=640750

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 0:4.18-7
- Drop gcj.
- Adapt to current guidelines.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Deepak Bhole <dbhole@redhat.com> - 0:4.18-4
- RPM was using pre-built jars before. Fixed that problem.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4.18-2
- fix license tag

* Tue Feb 19 2008 Dennis Gilmore <dennis@ausil.us> - 4.18-1
- update to 4.18
- spec contents pulled from RHEL5 srpm 
- fedora spec changelog
- update buildroot
- use jss from fedora for building

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.17-2jpp.7
- Autorebuild for GCC 4.3

* Fri Aug 11 2006 Vivek Lakshmanan <vivekl@redhat.com> 0:4.17-1jpp.7
- Rebuild with new naming convention.

* Mon Jul 24 2006 Vivek Lakshmanan <vivekl@redhat.com> 0:4.17-1jpp_6fc
- Add conditional native compilation.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.17-1jpp_5fc
- Rebuilt

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 0:4.17-1jpp_4fc
- fix release
- remove silly name, version, release defines.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:4.17-1jpp_3fc.1.1.2.1
- rebuild

* Tue Jul 11 2006 Archit Shah <ashah@redhat.com>
- add java-devel BuildRequires (bug #192530)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov  5 2005 Archit Shah <ashah@redhat.com> 0:4.17-1jpp_3fc
- Call javadoc with sourcepath to work aroung gjdoc bug (#170611)

* Thu Jan 27 2005 Gary Benson <gbenson@redhat.com> 0:4.17-1jpp_2fc
- Remove non-distributable files from the source tarball.

* Fri Jan 21 2005 Gary Benson <gbenson@redhat.com> 0:4.17-1jpp_1fc
- Build into Fedora.

* Tue Nov 16 2004 Fernando Nasser <fnasser@redhat.com> 0:4.17-1jpp_1rh
- Merge with upstream for upgrade

* Thu Aug 26 2004 Fernando Nasser <fnasser@redhat.com> 0:4.17-1jpp
- Upgrade to 4.17
- Rebuilt with Ant 1.6.2

* Fri Mar  5 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1-5jpp_1rh
- RH vacuuming
- added ldapjdk-javaxssl.patch to stop using com.sun.*

* Sun Sep 28 2003 David Walluck <david@anti-microsoft.org> 0:4.1-5jpp
- add Distribution and Vendor tags
- fix jpackage-utils requirement
- change gmake to %%__make
- break %%description lines

* Thu Mar 27 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org>
- Initial build.
