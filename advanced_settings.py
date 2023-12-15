#!/usr/bin/env python

import wx
import images as images
from runtime import *


# ============================================================================
#                               Class AdvancedSettings
# ============================================================================
class AdvancedSettings(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetTitle("Advanced Configuration Settings")

        vSizer = wx.BoxSizer(wx.VERTICAL)
        warning_sizer = wx.BoxSizer(wx.HORIZONTAL)
        warning_text = '''警告！
这是高级配置。
除非你知道你在做什么，
否则你不应该启用它。

你必须对你的设备发生的任何事情负责。
这个工具的编写是基于你熟悉下面这些概念的前提下的：
ADB，Magisk，Android和Root。
确保你知道你在做什么是你自己的责任。
    '''
        # warning label
        self.warning_label = wx.StaticText(parent=self, id=wx.ID_ANY, label=warning_text, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.ALIGN_CENTER_HORIZONTAL)
        self.warning_label.Wrap(-1)
        self.warning_label.SetForegroundColour(wx.Colour(255, 0, 0))
        warning_sizer.Add(self.warning_label, proportion=0, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=80)
        vSizer.Add(warning_sizer, proportion=0, flag=wx.EXPAND, border=5)

        # advanced options
        advanced_options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.advanced_options_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"Enable Advanced Options", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.advanced_options_checkbox.SetToolTip(u"Expert mode")
        advanced_options_sizer.Add(self.advanced_options_checkbox, proportion=0, flag=wx.ALL, border=5)
        vSizer.Add(advanced_options_sizer, proportion=0, flag=wx.EXPAND, border=5)

        # static line
        staticline = wx.StaticLine(parent=self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LI_HORIZONTAL)
        vSizer.Add(staticline, proportion=0, flag=wx.EXPAND, border=5)

        # gap
        # vSizer.Add((0, 20), proportion=0, flag=0, border=5)

        fgs1 = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        # this makes the second column expandable (index starts at 0)
        fgs1.AddGrowableCol(1, 1)

        # Magisk包名
        package_name_label = wx.StaticText(parent=self, label=u"Magisk包名")
        self.package_name = wx.TextCtrl(parent=self, id=-1, size=(-1, -1))
        self.package_name.SetToolTip(u"如果你已经隐藏了Magisk，\n请将此设置为隐藏的包名。")
        self.reset_magisk_pkg = wx.BitmapButton(parent=self, id=wx.ID_ANY, bitmap=wx.NullBitmap, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.BU_AUTODRAW)
        self.reset_magisk_pkg.SetBitmap(images.scan_24.GetBitmap())
        self.reset_magisk_pkg.SetToolTip(u"将包名重置为默认值：com.topjohnwu.magisk")
        package_name_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        package_name_sizer.Add(self.package_name, proportion=1, flag=wx.ALL, border=0)
        package_name_sizer.Add(self.reset_magisk_pkg, proportion=0, flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=5)
        # only add if we're on linux
        if sys.platform.startswith("linux"):
            # Linux 文件管理器
            file_explorer_label = wx.StaticText(self, label=u"Linux 文件管理器:")
            file_explorer_label.SetSize(self.package_name.GetSize())
            self.file_explorer = wx.TextCtrl(self, -1, size=(300, -1))
            self.file_explorer.SetToolTip(u"设置文件管理器的完整路径。\n默认值：Nautilus")
            file_explorer_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
            file_explorer_sizer.Add((20, 0), proportion=0, flag=wx.ALL, border=5)
            file_explorer_sizer.Add(self.file_explorer, proportion=0, flag=wx.LEFT, border=10)

            # Linux Shell
            shell_label = wx.StaticText(parent=self, label=u"Linux Shell:")
            shell_label.SetSize(self.package_name.GetSize())
            self.shell = wx.TextCtrl(parent=self, id=wx.ID_ANY, size=(300, -1))
            self.shell.SetToolTip(u"设置 Linux Shell 的完整路径。\n默认值：gnome-terminal")
            shell_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
            shell_sizer.Add((20, 0), proportion=0, flag=wx.ALL, border=5)
            shell_sizer.Add(self.shell, proportion=0, flag=wx.LEFT, border=10)


        # 提供补丁方法
        self.patch_methods_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"提供补丁方法", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.patch_methods_checkbox.SetToolTip(u"打补丁时将呈现选择方法的选项。")
        self.recovery_patch_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"修补恢复分区", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.recovery_patch_checkbox.SetToolTip(u"启用此选项将显示修补恢复分区的选项。\n除非您的设备较旧，否则应保持禁用状态。\n（大多数仅带有 Android 9 的 A-only 设备，传统 SAR）")

        # 使用 Busybox Shell
        self.use_busybox_shell_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"使用 Busybox Shell", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.use_busybox_shell_checkbox.SetToolTip(u"创建补丁时，如果勾选此选项，将使用 busybox ash 作为 shell。")

        # 启用低内存模式
        self.low_mem_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"系统内存较低", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.low_mem_checkbox.SetToolTip(u"使用此选项以牺牲速度来节省内存。")

        # 额外的 img 提取
        self.extra_img_extracts_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"额外的 img 提取", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.extra_img_extracts_checkbox.SetToolTip(u"勾选此选项且 payload.bin 中可用时\n还将提取 vendor_boot.img、vendor_kernel_boot.img、dtbo.img、super_empty.img")

        # 显示通知
        self.show_notifications_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"显示通知", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.show_notifications_checkbox.SetToolTip(u"勾选后，PixelFlasher 将显示系统吐司通知。")

        # 始终创建 boot.tar
        self.create_boot_tar_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"始终创建 boot.tar", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.create_boot_tar_checkbox.SetToolTip(u"勾选后，PixelFlasher 总是为打过补丁的启动文件创建 boot.tar。\n如果未勾选，只为三星固件创建 boot.tar。")
        self.create_boot_tar_checkbox.Disable()

        # 检查更新选项
        self.check_for_update_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"检查更新", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.check_for_update_checkbox.SetToolTip(u"在启动时检查可用更新")

        # 检查最小磁盘空间选项
        self.check_for_disk_space_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"检查最小磁盘空间 (5Gb)", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.check_for_disk_space_checkbox.SetToolTip(u"执行闪存前强制要求至少 5 Gb 的磁盘空间。\n这有助于避免存储相关问题。")

        # 检查 Bootloader 解锁选项
        self.check_for_bootloader_unlocked_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"检查 bootloader 解锁", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.check_for_bootloader_unlocked_checkbox.SetToolTip(u"在执行闪存前检查 bootloader 是否已解锁。")

        # 检查固件哈希有效性选项
        self.check_for_firmware_hash_validity_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"检查固件哈希有效性", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.check_for_firmware_hash_validity_checkbox.SetToolTip(u"检查图像文件名中是否包含 sha256 部分，以便检测 Pixel 兼容的图像。")

        # 强制代码页
        self.force_codepage_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"强制代码页为", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.force_codepage_checkbox.SetToolTip(u"使用指定的代码页，而不是系统代码页")
        self.code_page = wx.TextCtrl(parent=self, id=wx.ID_ANY, size=(-1, -1))

        # 删除捆绑库
        self.delete_bundled_libs_label = wx.StaticText(parent=self, id=wx.ID_ANY, label=u"删除捆绑库")
        self.delete_bundled_libs_label.SetToolTip(u"将列出的库从 PF 捆绑中删除，以便使用系统定义的库。")
        self.delete_bundled_libs = wx.SearchCtrl(self, style=wx.TE_LEFT)
        self.delete_bundled_libs.ShowCancelButton(True)
        self.delete_bundled_libs.SetDescriptiveText("示例：libreadline.so.8, libgdk*")
        self.delete_bundled_libs.ShowSearchButton(False)

        # 使用自定义字体
        self.use_custom_font_checkbox = wx.CheckBox(parent=self, id=wx.ID_ANY, label=u"使用自定义字体", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        self.use_custom_font_checkbox.SetToolTip(u"为等宽字体使用自定义字体\n可能需要重启 PixelFlasher 以正确应用于控制台窗口。")

        # Font Selection
        fonts = wx.FontEnumerator()
        fonts.EnumerateFacenames(wx.FONTENCODING_SYSTEM, fixedWidthOnly=True)
        font_list = fonts.GetFacenames(wx.FONTENCODING_SYSTEM, fixedWidthOnly=True)
        self.font = wx.ListBox(parent=self, id=wx.ID_ANY, size=(300, 100), choices=font_list)
        self.font_size = wx.SpinCtrl(parent=self, id=wx.ID_ANY, min=6, max=50, initial=self.Parent.config.pf_font_size)
        self.sample = wx.StaticText(parent=self, id=wx.ID_ANY, label="Sample ")
        fonts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fonts_sizer.Add(self.font, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=0)
        fonts_sizer.Add(self.font_size, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        fonts_sizer.Add(self.sample, proportion=1, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.font.SetSelection(-1)
        self.font_size.SetToolTip('Select font size')
        self._onFontSelect(None)

        # scrcpy 第一行控件，选择路径
        self.scrcpy_path_label = wx.StaticText(parent=self, id=wx.ID_ANY, label=u"Scrcpy 路径")
        self.srccpy_link = wx.BitmapButton(parent=self, id=wx.ID_ANY, bitmap=wx.NullBitmap, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.BU_AUTODRAW)
        self.srccpy_link.SetBitmap(bitmap=images.open_link_24.GetBitmap())
        self.srccpy_link.SetToolTip("下载 Scrcpy")
        self.scrcpy_path_picker = wx.FilePickerCtrl(parent=self, id=wx.ID_ANY, path=wx.EmptyString, message=u"选择 scrcpy 可执行文件", wildcard=u"Scrcpy 可执行文件 (*.exe;*)|*.exe;*", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.FLP_USE_TEXTCTRL)

        self.scrcpy_path_picker.SetToolTip("选择 scrcpy 可执行文件")
        self.scrcpy_h1sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.scrcpy_h1sizer.Add(window=self.scrcpy_path_label, proportion=0, flag=wx.EXPAND)
        self.scrcpy_h1sizer.AddSpacer(10)
        self.scrcpy_h1sizer.Add(window=self.srccpy_link, proportion=0, flag=wx.EXPAND)
        self.scrcpy_h1sizer.AddSpacer(10)
        self.scrcpy_h1sizer.Add(window=self.scrcpy_path_picker, proportion=1, flag=wx.EXPAND)

        # scrcpy 第二行标志
        self.scrcpy_flags = wx.SearchCtrl(self, style=wx.TE_LEFT)
        self.scrcpy_flags.ShowCancelButton(True)
        self.scrcpy_flags.SetDescriptiveText("标志/参数（例如：--video-bit-rate 2M --max-fps=30 --max-size 1024）")
        self.scrcpy_flags.ShowSearchButton(False)

        # 为 scrcpy 构建布局
        scrcpy_sb = wx.StaticBox(self, -1, "Scrcpy 设置")
        scrcpy_vsizer = wx.StaticBoxSizer(scrcpy_sb, wx.VERTICAL)
        scrcpy_vsizer.Add(self.scrcpy_h1sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        scrcpy_vsizer.Add(self.scrcpy_flags, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        #
        scrcpy_outer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scrcpy_outer_sizer.AddSpacer(20)
        scrcpy_outer_sizer.Add(scrcpy_vsizer, proportion=1, flag=wx.EXPAND, border=10)
        scrcpy_outer_sizer.AddSpacer(20)

        # add the widgets to the grid in two columns, first fix size, the second expandable.
        fgs1.Add(package_name_label, 0, wx.EXPAND)
        fgs1.Add(package_name_sizer, 1, wx.EXPAND)

        # Set Widget values from config
        self.advanced_options_checkbox.SetValue(self.Parent.config.advanced_options)
        self.package_name.SetValue(self.Parent.config.magisk)
        self.patch_methods_checkbox.SetValue(self.Parent.config.offer_patch_methods)
        self.recovery_patch_checkbox.SetValue(self.Parent.config.show_recovery_patching_option)
        self.use_busybox_shell_checkbox.SetValue(self.Parent.config.use_busybox_shell)
        self.low_mem_checkbox.SetValue(self.Parent.config.low_mem)
        self.extra_img_extracts_checkbox.SetValue(self.Parent.config.extra_img_extracts)
        self.show_notifications_checkbox.SetValue(self.Parent.config.show_notifications)
        self.create_boot_tar_checkbox.SetValue(self.Parent.config.create_boot_tar)
        self.check_for_update_checkbox.SetValue(self.Parent.config.update_check)
        self.check_for_disk_space_checkbox.SetValue(self.Parent.config.check_for_disk_space)
        self.check_for_bootloader_unlocked_checkbox.SetValue(self.Parent.config.check_for_bootloader_unlocked)
        self.check_for_firmware_hash_validity_checkbox.SetValue(self.Parent.config.check_for_firmware_hash_validity)
        self.force_codepage_checkbox.SetValue(self.Parent.config.force_codepage)
        self.delete_bundled_libs.SetValue(self.Parent.config.delete_bundled_libs)
        self.code_page.SetValue(str(self.Parent.config.custom_codepage))
        self.use_custom_font_checkbox.SetValue(self.Parent.config.customize_font)
        self.font.SetStringSelection(self.Parent.config.pf_font_face)

        if self.Parent.config.scrcpy and self.Parent.config.scrcpy['path'] != '' and os.path.exists(self.Parent.config.scrcpy['path']):
            self.scrcpy_path_picker.SetPath(self.Parent.config.scrcpy['path'])
        if self.Parent.config.scrcpy and self.Parent.config.scrcpy['flags'] != '':
            self.scrcpy_flags.SetValue(self.Parent.config.scrcpy['flags'])

        if sys.platform.startswith("linux"):
            self.file_explorer.SetValue(self.Parent.config.linux_file_explorer)
            self.shell.SetValue(self.Parent.config.linux_shell)

            # only add if we're on linux
            fgs1.Add(file_explorer_label, 0, wx.EXPAND)
            fgs1.Add(file_explorer_sizer, 1, wx.EXPAND)
            fgs1.Add(shell_label, 0, wx.EXPAND)
            fgs1.Add(shell_sizer, 1, wx.EXPAND)

        fgs1.Add(self.patch_methods_checkbox, 0, wx.EXPAND)
        fgs1.Add(self.recovery_patch_checkbox, 0, wx.EXPAND)

        fgs1.Add(self.use_busybox_shell_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.low_mem_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.extra_img_extracts_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.show_notifications_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.create_boot_tar_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.check_for_update_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.check_for_disk_space_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.check_for_bootloader_unlocked_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.check_for_firmware_hash_validity_checkbox, 0, wx.EXPAND)
        fgs1.Add((0, 0))

        fgs1.Add(self.force_codepage_checkbox, 0, wx.EXPAND)
        fgs1.Add(self.code_page, 1, wx.EXPAND)

        fgs1.Add(self.delete_bundled_libs_label, 0, wx.EXPAND)
        fgs1.Add(self.delete_bundled_libs, 1, wx.EXPAND)

        fgs1.Add(self.use_custom_font_checkbox, 0, wx.EXPAND)
        fgs1.Add(fonts_sizer, 1, wx.EXPAND)

        # add flexgrid to vSizer
        vSizer.Add(fgs1, proportion=0, flag=wx.ALL | wx.EXPAND, border=20)

        # Add more stuff after the flexgrid
        vSizer.Add(scrcpy_outer_sizer, proportion=1, flag=wx.EXPAND)

        # gap
        vSizer.Add((0, 20), proportion=0, flag=0, border=5)

        # buttons
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add((0, 0), proportion=1, flag=wx.EXPAND, border=5)
        self.ok_button = wx.Button(parent=self, id=wx.ID_ANY, label=u"OK", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        buttons_sizer.Add(self.ok_button, proportion=0, flag=wx.ALL, border=20)
        self.cancel_button = wx.Button(parent=self, id=wx.ID_ANY, label=u"Cancel", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0)
        buttons_sizer.Add(self.cancel_button, proportion=0, flag=wx.ALL, border=20)
        buttons_sizer.Add((0, 0), proportion=1, flag=wx.EXPAND, border=5)
        vSizer.Add(buttons_sizer, proportion=0, flag=wx.EXPAND, border=5)

        self.SetSizer(vSizer)
        self.Layout()

        # Connect Events
        self.ok_button.Bind(wx.EVT_BUTTON, self._onOk)
        self.cancel_button.Bind(wx.EVT_BUTTON, self._onCancel)
        self.font.Bind(wx.EVT_LISTBOX, self._onFontSelect)
        self.font_size.Bind(wx.EVT_SPINCTRL, self._onFontSelect)
        self.reset_magisk_pkg.Bind(wx.EVT_BUTTON, self._onResetMagiskPkg)
        self.patch_methods_checkbox.Bind(wx.EVT_CHECKBOX, self._on_offer_patch_methods)
        self.use_custom_font_checkbox.Bind(wx.EVT_CHECKBOX, self._on_use_custom_fontface)

        # Enable / Disable Widgets
        self.enable_disable_widgets()

        # Autosize the dialog
        self.SetSizerAndFit(vSizer)

    def enable_disable_widgets(self):
        if self.patch_methods_checkbox.GetValue():
            self.recovery_patch_checkbox.Enable()
        else:
            self.recovery_patch_checkbox.Disable()
        if self.use_custom_font_checkbox.GetValue():
            self.font.Enable()
            self.font_size.Enable()
            self.sample.Enable()
        else:
            self.font.Disable()
            self.font_size.Disable()
            self.sample.Disable()

    def _on_offer_patch_methods(self, event):
        self.enable_disable_widgets()

    def _on_use_custom_fontface(self, event):
        self.enable_disable_widgets()

    def _onFontSelect(self, evt):
        facename = self.font.GetStringSelection()
        size = self.font_size.GetValue()
        font = wx.Font(size, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False, faceName=facename)
        self.sample.SetLabel(facename)
        self.sample.SetFont(font)
        self.Refresh()

    def _onResetMagiskPkg(self, e):
        self.package_name.Label = 'com.topjohnwu.magisk'

    def _onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def _onOk(self, e):
        if self.advanced_options_checkbox.GetValue() != self.Parent.config.advanced_options:
            print(f"Setting Enable Advanced Options to: {self.advanced_options_checkbox.GetValue()}")
        self.Parent.config.advanced_options = self.advanced_options_checkbox.GetValue()

        if self.patch_methods_checkbox.GetValue() != self.Parent.config.offer_patch_methods:
            print(f"Setting Offer Patch Methods to: {self.patch_methods_checkbox.GetValue()}")
        self.Parent.config.offer_patch_methods = self.patch_methods_checkbox.GetValue()

        if self.recovery_patch_checkbox.GetValue() != self.Parent.config.show_recovery_patching_option:
            print(f"Setting Offer Patch Methods to: {self.recovery_patch_checkbox.GetValue()}")
        self.Parent.config.show_recovery_patching_option = self.recovery_patch_checkbox.GetValue()

        if self.use_busybox_shell_checkbox.GetValue() != self.Parent.config.use_busybox_shell:
            print(f"Setting Use Busybox Shell to: {self.use_busybox_shell_checkbox.GetValue()}")
        self.Parent.config.use_busybox_shell = self.use_busybox_shell_checkbox.GetValue()

        if self.low_mem_checkbox.GetValue() != self.Parent.config.low_mem:
            print(f"Setting Low Memory to: {self.low_mem_checkbox.GetValue()}")
        self.Parent.config.low_mem = self.low_mem_checkbox.GetValue()
        set_low_memory(self.low_mem_checkbox.GetValue())

        if self.extra_img_extracts_checkbox.GetValue() != self.Parent.config.extra_img_extracts:
            print(f"Setting Extra img extraction to: {self.extra_img_extracts_checkbox.GetValue()}")
        self.Parent.config.extra_img_extracts = self.extra_img_extracts_checkbox.GetValue()

        if self.show_notifications_checkbox.GetValue() != self.Parent.config.show_notifications:
            print(f"Setting Show notifications to: {self.show_notifications_checkbox.GetValue()}")
        self.Parent.config.show_notifications = self.show_notifications_checkbox.GetValue()

        if self.create_boot_tar_checkbox.GetValue() != self.Parent.config.create_boot_tar:
            print(f"Setting Always create boot.tar: {self.create_boot_tar_checkbox.GetValue()}")
        self.Parent.config.create_boot_tar = self.create_boot_tar_checkbox.GetValue()

        if self.check_for_update_checkbox.GetValue() != self.Parent.config.update_check:
            print(f"Setting Check for updates to: {self.check_for_update_checkbox.GetValue()}")
        self.Parent.config.update_check = self.check_for_update_checkbox.GetValue()

        if self.check_for_disk_space_checkbox.GetValue() != self.Parent.config.check_for_disk_space:
            print(f"Setting Check for Miminum Disk Space to: {self.check_for_disk_space_checkbox.GetValue()}")
        self.Parent.config.check_for_disk_space = self.check_for_disk_space_checkbox.GetValue()

        if self.check_for_bootloader_unlocked_checkbox.GetValue() != self.Parent.config.check_for_bootloader_unlocked:
            print(f"Setting Check for Miminum Disk Space to: {self.check_for_bootloader_unlocked_checkbox.GetValue()}")
        self.Parent.config.check_for_bootloader_unlocked = self.check_for_bootloader_unlocked_checkbox.GetValue()

        if self.check_for_firmware_hash_validity_checkbox.GetValue() != self.Parent.config.check_for_firmware_hash_validity:
            print(f"Setting Check for Firmware Hash Validity to: {self.check_for_firmware_hash_validity_checkbox.GetValue()}")
        self.Parent.config.check_for_firmware_hash_validity = self.check_for_firmware_hash_validity_checkbox.GetValue()

        if self.package_name.GetValue():
            with contextlib.suppress(Exception):
                if self.package_name.GetValue() != self.Parent.config.magisk:
                    print(f"Setting Magisk Package Name to: {self.package_name.GetValue()}")
                set_magisk_package(self.package_name.GetValue())
                self.Parent.config.magisk = self.package_name.GetValue()

        if sys.platform.startswith("linux"):
            with contextlib.suppress(Exception):
                if self.file_explorer.GetValue() != self.Parent.config.linux_file_explorer:
                    print(f"Setting Linux File Explorer to: {self.file_explorer.GetValue()}")
                self.Parent.config.linux_file_explorer = self.file_explorer.GetValue()

            with contextlib.suppress(Exception):
                if self.shell.GetValue() != self.Parent.config.linux_shell:
                    print(f"Setting Linux Shell to: {self.shell.GetValue()}")
                set_linux_shell(self.shell.GetValue())
                self.Parent.config.linux_shell = self.shell.GetValue()

        self.Parent.config.force_codepage = self.force_codepage_checkbox.GetValue()
        if self.code_page.GetValue() and self.code_page.GetValue().isnumeric():
            self.Parent.config.custom_codepage = int(self.code_page.GetValue())

        value = self.delete_bundled_libs.GetValue()
        if value is None:
            value = ''
        if value != self.Parent.config.delete_bundled_libs:
            print(f"Setting Delete bundled libs to: {value}")
            self.Parent.config.delete_bundled_libs = value

        font_settings_changed = False
        if self.use_custom_font_checkbox.GetValue() != self.Parent.config.customize_font:
            print("Enabling Custom Font")
            font_settings_changed = True
        if self.font.GetStringSelection() != self.Parent.config.pf_font_face:
            print(f"Setting Application Font to: {self.font.GetStringSelection()}")
            if self.use_custom_font_checkbox.GetValue():
                font_settings_changed = True
        if self.font_size.GetValue() != self.Parent.config.pf_font_size:
            print(f"Setting Application Font Size to: {self.font_size.GetValue()}")
            if self.use_custom_font_checkbox.GetValue():
                font_settings_changed = True
        self.Parent.config.customize_font = self.use_custom_font_checkbox.GetValue()
        self.Parent.config.pf_font_face = self.font.GetStringSelection()
        self.Parent.config.pf_font_size = self.font_size.GetValue()

        value = self.scrcpy_path_picker.GetPath()
        if value is None:
            value = ''
        if value != self.Parent.config.scrcpy['path'] and os.path.exists(value):
            print(f"Setting scrcpy path path to: {value}")
            self.Parent.config.scrcpy['path'] = value

        value = self.scrcpy_flags.GetValue()
        if value is None:
            value = ''
        if value != self.Parent.config.scrcpy['flags']:
            print(f"Setting scrcpy flags to: {value}")
            self.Parent.config.scrcpy['flags'] = value

        # update the runtime config
        set_config(self.Parent.config)

        if font_settings_changed:
            self.Parent.set_ui_fonts()

        self.EndModal(wx.ID_OK)
