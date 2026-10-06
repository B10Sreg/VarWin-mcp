# Maintainer: B10Sreg <iam171181@gmail.com>
pkgname=varwin-bin
pkgver=18.5.512
pkgrel=2
pkgdesc="Varwin XRMS - 3D/VR Platform and Creation Suite for Linux"
arch=('x86_64')
url="https://varwin.com"
license=('custom:proprietary')
depends=(
    'gtk3'
    'libnotify'
    'nss'
    'libxss'
    'libxtst'
    'xdg-utils'
    'at-spi2-core'
    'libsecret'
    'ffmpeg'
    'espeak-ng'
    'xorg-xdpyinfo'
)
optdepends=(
    'vulkan-driver: Hardware accelerated 3D graphics and Vulkan support'
    'nvidia-utils: Proprietary NVIDIA graphics driver support'
    'monado: Open source OpenXR runtime for VR headsets'
    'openxr: OpenXR loader for VR support'
)
provides=('varwin' 'varwin-18')
conflicts=('varwin' 'varwin-18')
install=varwin.install
# ВАЖНО: 'staticlibs' обязателен для работы .NET Core зависимостей
options=('!strip' '!debug' 'staticlibs')

source=(
    "Varwin_${pkgver}.deb::https://dist.varwin.com/debian/stable/18/pool/non-free/v/varwin-18/Varwin%20${pkgver}.deb"
    "libicu63_63.1-6+deb10u3_amd64.deb::https://dist.varwin.com/debian/stable/18/pool/non-free/i/icu/libicu63_63.1-6+deb10u3_amd64.deb"
    "libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb::http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb"
    "varwin.sh"
    "varwin-client.sh"
    "varwin18.conf"
    "Varwin18.desktop"
    "VarwinClient18.desktop"
)

sha256sums=(
    'a62e5beda13e193426e1a655f90ce2298cfca48743eede29ccab2b26401cbe70'
    '38f65aaec4ee088f65330cf636c1cd6edef38109c80559836ecf38e2390a5761'
    '7cf39d70a639017d1dd7c8d36daa2258063608688e449fddf40ffdd46f992a78'
    '778fcab9f844d7c73ce8c3f4ab37ba5980359b7294d5da302ac89ed42ff04cf7'
    'a9ec0113502eb6d2bf18011ddb5f325a85646e555eb51d85f081a9bf5299ca73'
    '620de3bec9ccf2ae35c04bd1c759824cef7b7d3e6fc466c55ce89765fa0cf23a'
    '45a46d054ce112bd41788a087bfeb0302eab69930ae401eb39d411e3064e718f'
    '1b4409a53670706b54695f8a51425609d2af5215ca5c1e58647d757b5c1d1900'
)

package() {
    # 1. Unpack Varwin main payload
    cd "${srcdir}"
    ar x "Varwin_${pkgver}.deb" data.tar.xz
    tar -xf data.tar.xz -C "${pkgdir}/"
    rm -f data.tar.xz

    # 2. Extract ICU 63 compatibility libraries
    mkdir -p "${srcdir}/icu"
    ar p "libicu63_63.1-6+deb10u3_amd64.deb" data.tar.xz | tar -xJf - -C "${srcdir}/icu"
    install -d "${pkgdir}/opt/Varwin18/lib"
    cp -a "${srcdir}"/icu/usr/lib/x86_64-linux-gnu/libicu* "${pkgdir}/opt/Varwin18/lib/"

    # 3. Extract OpenSSL 1.1 compatibility libraries
    mkdir -p "${srcdir}/ssl"
    ar p "libssl1.1_1.1.1f-1ubuntu2.24_amd64.deb" data.tar.xz | tar -xJf - -C "${srcdir}/ssl"
    cp -a "${srcdir}"/ssl/usr/lib/x86_64-linux-gnu/libssl* "${pkgdir}/opt/Varwin18/lib/"
    cp -a "${srcdir}"/ssl/usr/lib/x86_64-linux-gnu/libcrypto* "${pkgdir}/opt/Varwin18/lib/"

    # 4. Copy compatibility libraries to .NET Core and backend services
    cp -a "${pkgdir}"/opt/Varwin18/lib/* "${pkgdir}/opt/Varwin18/services/" 2>/dev/null || true
    cp -a "${pkgdir}"/opt/Varwin18/lib/* "${pkgdir}/opt/Varwin18/services/client/VarwinMigratorService/" 2>/dev/null || true
    cp -a "${pkgdir}"/opt/Varwin18/lib/* "${pkgdir}/opt/Varwin18/services/client/UrlSchemaLauncher/" 2>/dev/null || true
    cp -a "${pkgdir}"/opt/Varwin18/lib/* "${pkgdir}/opt/Varwin18/services/converter/" 2>/dev/null || true

    # 5. Patch Unity Client for Vulkan swapchain stability
    if [ -f "${pkgdir}/opt/Varwin18/services/client/VarwinClient" ]; then
        mv "${pkgdir}/opt/Varwin18/services/client/VarwinClient" "${pkgdir}/opt/Varwin18/services/client/VarwinClient.real"
    fi
    install -Dm755 "${srcdir}/varwin-client.sh" "${pkgdir}/opt/Varwin18/services/client/VarwinClient"

    # 6. Install launchers and system wrappers
    install -Dm755 "${srcdir}/varwin.sh" "${pkgdir}/usr/bin/varwin"
    install -d "${pkgdir}/usr/bin"
    ln -sf varwin "${pkgdir}/usr/bin/varwin-18"

    # 7. Install ld.so config for compatibility libraries
    install -Dm644 "${srcdir}/varwin18.conf" "${pkgdir}/etc/ld.so.conf.d/varwin18.conf"

    # 8. Install desktop entries
    install -Dm644 "${srcdir}/Varwin18.desktop" "${pkgdir}/usr/share/applications/Varwin18.desktop"
    install -Dm644 "${srcdir}/VarwinClient18.desktop" "${pkgdir}/usr/share/applications/VarwinClient18.desktop"

    # 9. Chrome sandbox permissions
    if [ -f "${pkgdir}/opt/Varwin18/chrome-sandbox" ]; then
        chmod 4755 "${pkgdir}/opt/Varwin18/chrome-sandbox" 2>/dev/null || true
    fi
}
