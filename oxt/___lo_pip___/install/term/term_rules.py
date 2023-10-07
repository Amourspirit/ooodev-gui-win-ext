from __future__ import annotations
from typing import List, Type
from .term_proto import TermProto
from .gnome_terminal import GnomeTerminal
from .win_terminal import WindowsTerminal
from .mac_terminal import MacTerminal
from ...config import Config


class TermRules:
    """Manages rules for Versions"""

    def __init__(self, auto_register: bool = True) -> None:
        """
        Initialize VerRules

        Args:
            auto_register (bool, optional): Determines if know rules are automatically registered. Defaults to True.
        """
        self._rules: List[Type[TermProto]] = []
        if auto_register:
            self._register_known_rules()

    def __len__(self) -> int:
        return len(self._rules)

    # region Methods

    def register_rule(self, rule: Type[TermProto]) -> None:
        """
        Register rule

        Args:
            rule (TermProto): Rule to register
        """
        if rule in self._rules:
            # msg = f"{self.__class__.__name__}.register_rule() Rule is already registered"
            # log.logger.warning(msg)
            return
        self._reg_rule(rule=rule)

    def unregister_rule(self, rule: Type[TermProto]):
        """
        Unregister Rule

        Args:
            rule (TermProto): Rule to unregister

        Raises:
            ValueError: If an error occurs
        """
        try:
            self._rules.remove(rule)
        except ValueError as e:
            msg = f"{self.__class__.__name__}.unregister_rule() Unable to unregister rule."
            raise ValueError(msg) from e

    def _reg_rule(self, rule: Type[TermProto]):
        self._rules.append(rule)

    def _register_known_rules(self):
        cfg = Config()
        if cfg.is_win:
            self._reg_rule(rule=WindowsTerminal)
        elif cfg.is_linux:
            self._reg_rule(rule=GnomeTerminal)
        elif cfg.is_mac:
            self._reg_rule(rule=MacTerminal)

    def get_terminal(self) -> TermProto | None:
        """
        Get terminal if it is a match.

        Returns:
            TermProto | None: Terminal if it is a match; Otherwise, None
        """

        for rule in self._rules:
            inst = rule()
            if inst.get_is_match():
                return inst
        return None

    # endregion Methods
