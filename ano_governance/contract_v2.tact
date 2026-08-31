// Смарт-контракт v2 для управления участниками и голосованием в АНО "КТО с СВО"
// Основан на Уставе АНО "КТО с СВО" (ANO.md)

import "@stdlib/deploy";
import "@stdlib/ownable";

// Структура для хранения информации о предложении (для Общего собрания - Устав 4.2, 4.3)
struct Proposal {
    description: String;        // Описание предложения или ссылка на детали
    proposer: Address;          // Адрес инициатора предложения
    creationTime: Int as uint64;// Время создания (timestamp)
    votingDeadline: Int as uint64;// Время окончания голосования (timestamp)
    votesFor: Int;              // Количество голосов "за"
    votesAgainst: Int;          // Количество голосов "против"
    isExecuted: Bool;           // Статус: исполнено ли предложение
    // Связано с Устав Глава 4, особенно 4.2, 4.3
}

// Структура для хранения информации об Участнике АНО (Устав Глава 3)
// В данном контракте информация об участнике сведена к его votingPower.
// Детальная информация (физ/юр лицо) ведется вне блокчейна.
// struct MemberData {
//     votingPower: Int;
//     memberSince: Int as uint64;
// }

struct LastMessage {
    last_message: String?;
    last_sender: Address?;
    last_receiver: Address?;
}

trait Stats {
    counter: Int;
    last_message: String?;
    last_sender: Address?;
    last_receiver: Address?;

    get fun get_count(): Int {
        return self.counter;
    }

    get fun get_last(): LastMessage {
        return
            LastMessage{
                last_message: self.last_message,
                last_sender: self.last_sender,
                last_receiver: self.last_receiver
            };
    }
}

// Трейт для типов участников АНО (Устав 3.2) - для будущих расширений
// Устав 3.2: "Участниками АНО могут быть физические и юридические лица..."
// AI-агенты не являются участниками (Устав 3.3)
trait MemberTypeOptions {
    virtual const PHYSICAL_PERSON: Int = 1;
    virtual const LEGAL_ENTITY: Int = 2;
}

// Структура для представления целей АНО (Устав 2.1)
struct AnoktoGoal {
    goalId: Int;
    description: String;
    // Связано с Устав 2.1
}

// Структура для представления видов деятельности АНО (Устав 2.2)
struct AnoktoActivity {
    activityId: Int;
    description: String;
    // Связано с Устав 2.2
}

// Трейт для источников формирования имущества (Устав 5.1) - для будущих расширений
trait AssetSourceTypeOptions {
  virtual const MEMBERSHIP_FEES: Int = 1;
  virtual const DONATIONS: Int = 2;
  virtual const PROJECT_INCOME: Int = 3;
  // AI_AGENT_INCOME удалено, т.к. AI агенты - инструменты, а не источники дохода напрямую в этом контексте
}

// Структура для описания процесса голосования (Устав 4.3)
struct VotingProcessConfig {
    quorumPercent: Int; // Минимальный % участия от общего числа голосов для кворума (Устав 4.3 "не менее половины")
    defaultVotingDurationDays: Int; // Продолжительность голосования по умолчанию в днях
}

contract AnoKtoV2 with Deployable, OwnableTransferable, Stats {
    // --- Состояние контракта ---
    counter: Int = 0;
    last_message: String? = null;
    last_sender: Address? = null;
    last_receiver: Address? = null;

    owner: Address; // Владелец контракта (из OwnableTransferable), обычно совпадает с chairman при инициализации
                    // Устав 4.5 Председатель Правления действует от имени АНО

    chairman: Address; // Председатель Правления (Устав 4.5)
                       // В данном контракте председатель выполняет ключевые управляющие функции

    // Карта Учредителей (Устав 3.1)
    // Ключ: адрес учредителя, Значение: true
    founders: map<Address, Bool>;

    // Карта Участников (Устав Глава 3)
    // Ключ: адрес участника, Значение: сила голоса (votingPower)
    members: map<Address, Int>;
    totalMemberVotingPower: Int = 0; // Суммарная сила голосов всех участников

    // Карта Предложений (Устав 4.2)
    // Ключ: ID предложения, Значение: Proposal struct
    proposals: map<Int, Proposal>;
    nextProposalId: Int = 0; // Счетчик для ID предложений

    // Параметры голосования (Устав 4.3)
    votingConfig: VotingProcessConfig;

    // Список целей АНО (Устав 2.1)
    anoktoGoals: map<Int, AnoktoGoal>;
    nextGoalId: Int = 0;

    // Список видов деятельности АНО (Устав 2.2)
    anoktoActivities: map<Int, AnoktoActivity>;
    nextActivityId: Int = 0;

    // --- Инициализация ---
    init(initialChairman: Address, quorumPercentage: Int, defaultVoteDurationDays: Int){
        self.owner = initialChairman; // Устав 4.5
        self.chairman = initialChairman; // Устав 4.5
        self.founders.set(initialChairman, true); // Устав 3.1 - первый учредитель
        self.votingConfig = VotingProcessConfig{
            quorumPercent: quorumPercentage, // e.g., 50 for 50%
            defaultVotingDurationDays: defaultVoteDurationDays
        };
        // Устав 3.3: "AI-агенты ... не являются самостоятельными учредителями или участниками."
        // Поэтому отдельного управления AI-агентами как голосующими единицами в контракте нет.
        // Их использование - это инструментальная поддержка деятельности, решения принимают участники/органы АНО.
    }

    // --- Управление Участниками (Устав Глава 3) ---

    // Добавление участника (Устав 3.6 - порядок определяется внутренними положениями, здесь - Председателем)
    fun addMember(memberAddr: Address, votingPower: Int) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN"); // Устав 4.5
        require(votingPower > 0, "ANOV2_ERR_VOTING_POWER_POSITIVE");
        require(!self.members.exists(memberAddr), "ANOV2_ERR_MEMBER_EXISTS");

        self.members.set(memberAddr, votingPower);
        self.totalMemberVotingPower += votingPower;
        // TODO: Emit event MemberAdded
    }

    // Удаление участника (Устав 3.4 - добровольный выход; 3.6 - порядок определяется...)
    fun removeMember(memberAddr: Address) {
        require(sender() == self.chairman || sender() == memberAddr, "ANOV2_ERR_CHAIRMAN_OR_SELF"); // Председатель или сам участник
        require(self.members.exists(memberAddr), "ANOV2_ERR_MEMBER_NOT_FOUND");

        let oldPower: Int = self.members.get(memberAddr)!!;
        self.totalMemberVotingPower -= oldPower;
        self.members.del(memberAddr);
        // TODO: Emit event MemberRemoved
    }

    // Обновление силы голоса участника
    fun updateMemberVotingPower(memberAddr: Address, newVotingPower: Int) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN");
        require(self.members.exists(memberAddr), "ANOV2_ERR_MEMBER_NOT_FOUND");
        require(newVotingPower > 0, "ANOV2_ERR_VOTING_POWER_POSITIVE");

        let oldPower: Int = self.members.get(memberAddr)!!;
        self.totalMemberVotingPower = (self.totalMemberVotingPower - oldPower) + newVotingPower;
        self.members.set(memberAddr, newVotingPower);
        // TODO: Emit event MemberVotingPowerUpdated
    }

    get fun getMemberVotingPower(memberAddr: Address): Int? {
        return self.members.get(memberAddr);
    }

    get fun isMember(memberAddr: Address): Bool {
        return self.members.exists(memberAddr);
    }

    get fun getTotalMemberVotingPower(): Int {
        return self.totalMemberVotingPower;
    }

    // --- Управление Учредителями (Устав 3.1) ---
    // В текущей версии учредитель добавляется при init. Функции для динамического добавления/удаления учредителей не предусмотрены,
    // т.к. Устав определяет их на момент создания. Это может быть изменено решением Общего Собрания (Устав 6.1).
    get fun isFounder(addr: Address): Bool {
        return self.founders.exists(addr);
    }

    // --- Управление Предложениями и Голосованием (Устав Глава 4) ---

    // Создание предложения (Устав 3.4 - участники вносят предложения; Устав 4.2 - компетенция Общего собрания)
    fun createProposal(description: String, votingDurationDaysOverride: Int?) {
        // Участники (Устав 3.4) или Председатель (как организатор, Устав 4.5) могут инициировать
        require(self.members.exists(sender()) || sender() == self.chairman, "ANOV2_ERR_MEMBER_OR_CHAIRMAN_PROPOSAL");

        let durationDays: Int = self.votingConfig.defaultVotingDurationDays;
        if (votingDurationDaysOverride != null) {
            require(votingDurationDaysOverride!! > 0, "ANOV2_ERR_DURATION_POSITIVE");
            durationDays = votingDurationDaysOverride!!;
        }
        let votingDeadline: Int = now() + (durationDays * 60 * 60 * 24);
        let proposalId: Int = self.nextProposalId;

        self.proposals.set(proposalId, Proposal{
            description: description,
            proposer: sender(),
            creationTime: now(),
            votingDeadline: votingDeadline,
            votesFor: 0,
            votesAgainst: 0,
            isExecuted: false
        });
        self.nextProposalId += 1;
        // TODO: Emit event ProposalCreated(proposalId, sender(), description, votingDeadline)
    }

    // Голосование по предложению (Устав 4.3)
    fun vote(proposalId: Int, castVoteFor: Bool) {
        require(self.members.exists(sender()), "ANOV2_ERR_ONLY_MEMBERS_VOTE"); // Только участники голосуют
        require(self.proposals.exists(proposalId), "ANOV2_ERR_PROPOSAL_NOT_FOUND");

        let p: Proposal = self.proposals.get(proposalId)!!;
        require(now() <= p.votingDeadline, "ANOV2_ERR_VOTING_ENDED");
        require(!p.isExecuted, "ANOV2_ERR_PROPOSAL_EXECUTED");

        // TODO: Предотвращение повторного голосования (потребует хранения, кто уже проголосовал по этому предложению)
        // map<Int, map<Address, Bool>> proposalVoters; // proposalId -> (voterAddr -> hasVoted)
        // require(!self.proposalVoters.get(proposalId)?.exists(sender()), "ANOV2_ERR_ALREADY_VOTED");

        let voterPower: Int = self.members.get(sender())!!;
        if (castVoteFor) {
            p.votesFor += voterPower;
        } else {
            p.votesAgainst += voterPower;
        }
        self.proposals.set(proposalId, p);
        // self.proposalVoters.get(proposalId)?.set(sender(), true); // Отметить, что проголосовал
        // TODO: Emit event Voted(proposalId, sender(), castVoteFor, voterPower)
    }

    // Получение информации о предложении
    get fun getProposal(proposalId: Int): Proposal? {
        return self.proposals.get(proposalId);
    }

    // Определение статуса предложения (Устав 4.3)
    get fun getProposalStatus(proposalId: Int): String {
        require(self.proposals.exists(proposalId), "ANOV2_ERR_PROPOSAL_NOT_FOUND");
        let p: Proposal = self.proposals.get(proposalId)!!;

        if (p.isExecuted) {
            return "EXECUTED";
        }
        if (now() <= p.votingDeadline) {
            return "ACTIVE";
        }

        // Голосование завершено, определяем результат
        // 1. Проверка кворума по участию (Устав 4.3 "при наличии не менее половины от общего числа участников")
        //    Интерпретируем как: сумма голосов (за+против) должна составлять quorumPercent от totalMemberVotingPower
        let totalVotesCast: Int = p.votesFor + p.votesAgainst;
        let requiredVotesForQuorum: Int = (self.totalMemberVotingPower * self.votingConfig.quorumPercent) / 100;

        if (self.totalMemberVotingPower == 0) { // Edge case, no members with voting power
             return "FAILED_NO_VOTERS";
        }
        if (totalVotesCast < requiredVotesForQuorum && self.totalMemberVotingPower > 0) {
            return "FAILED_QUORUM_NOT_MET";
        }

        // 2. Простое большинство голосов (Устав 4.3 "Решения принимаются простым большинством голосов")
        if (p.votesFor > p.votesAgainst) {
            return "PASSED_PENDING_EXECUTION";
        } else if (p.votesAgainst > p.votesFor) {
            return "FAILED_AGAINST";
        } else {
            return "FAILED_TIE";
        }
    }

    // Отметка предложения как исполненного (Устав 4.5 - Председатель организует выполнение решений)
    fun markProposalExecuted(proposalId: Int) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN");
        require(self.proposals.exists(proposalId), "ANOV2_ERR_PROPOSAL_NOT_FOUND");

        let p: Proposal = self.proposals.get(proposalId)!!;
        require(now() > p.votingDeadline, "ANOV2_ERR_VOTING_STILL_ACTIVE");
        require(!p.isExecuted, "ANOV2_ERR_PROPOSAL_ALREADY_EXECUTED");

        // Перепроверка условий прохождения перед исполнением
        let status: String = self.getProposalStatus(proposalId);
        require(status == "PASSED_PENDING_EXECUTION", "ANOV2_ERR_PROPOSAL_NOT_PASSED");

        self.proposals.set(proposalId, p{isExecuted = true});
        // TODO: Emit event ProposalExecuted(proposalId, chairman)
    }

    // --- Управление Целями и Видами Деятельности (Устав Глава 2) ---
    // Устав 4.2: "Определение основных направлений деятельности АНО" - компетенция Общего собрания.
    // Добавление конкретных целей/активностей здесь делегировано Председателю как исполнителю.

    fun addAnoktoGoal(description: String) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN");
        let goalId: Int = self.nextGoalId;
        self.anoktoGoals.set(goalId, AnoktoGoal{goalId: goalId, description: description});
        self.nextGoalId += 1;
    }

    get fun getAnoktoGoal(goalId: Int): AnoktoGoal? {
        return self.anoktoGoals.get(goalId);
    }

    fun addAnoktoActivity(description: String) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN");
        let activityId: Int = self.nextActivityId;
        self.anoktoActivities.set(activityId, AnoktoActivity{activityId: activityId, description: description});
        self.nextActivityId += 1;
    }

    get fun getAnoktoActivity(activityId: Int): AnoktoActivity? {
        return self.anoktoActivities.get(activityId);
    }

    // --- Функции из trait Stats и общие receive ---
    // Эти функции не являются прямой реализацией Устава, а скорее служебные.
    // Их следует использовать с осторожностью, особенно _storeStats, если она позволяет обходить проверки доступа.

    receive("Repeat"){
        self.requireOwner(); // Только владелец (изначально chairman)
        send(SendParameters{
                to: self.last_receiver!!,
                value: 0,
                mode: SendRemainingValue,
                body: self.last_message!!.asComment()
            }
        );
        self.counter += 1;
    }

    receive("Return"){
        self.requireOwner(); // Только владелец
        send(SendParameters{
                to: self.last_sender!!,
                value: 0,
                mode: SendRemainingValue,
                body: self.last_message!!.asComment()
            }
        );
        self.counter += 1;
    }

    receive(str: String){
        // Любой может отправить строку, она пересылается владельцу
        send(SendParameters{to: self.owner, value: 0, mode: SendRemainingValue, body: str.asComment()});
        self.storeStats(sender(), self.owner, str);
    }

    fun storeStats(msgSender: Address, msgReceiver: Address, msgBody: String) {
        self.counter += 1;
        self.last_message = msgBody;
        self.last_sender = msgSender;
        self.last_receiver = msgReceiver;
    }

    // ВНИМАНИЕ: Функция _storeStats из оригинального контракта.
    // Она напрямую вызывает addMember, addAIAgent и т.д. БЕЗ ПРОВЕРКИ sender() == self.chairman.
    // Это означает, что если эту функцию можно вызвать извне с произвольным Slice,
    // то ограничения доступа в addMember и других функциях могут быть обойдены.
    // В текущей версии контракта AIAgent функции удалены.
    // Для безопасности, такую функцию следует либо сделать internal, либо вызывать только после проверки прав доступа.
    // В данной версии я оставляю ее как есть для сравнения, но рекомендую пересмотреть ее использование.
    fun _storeStatsByOwner(msg: Slice) {
        self.requireOwner(); // Добавлена проверка, что только владелец может вызывать эту низкоуровневую функцию

        let originalOp: Int = msg.loadInt(32);
        let op: Int = originalOp;

        if (op == 1) { // Добавить участника
            // require(sender() == self.chairman, "Only chairman can add members"); // Проверка уже сделана requireOwner
            let memberAddr: Address = msg.loadAddress();
            let votingPower: Int = msg.loadInt(32);
            // Прямой вызов без доп. проверок из addMember, т.к. sender() уже проверен как owner/chairman
            if (!self.members.exists(memberAddr) && votingPower > 0) {
                 self.members.set(memberAddr, votingPower);
                 self.totalMemberVotingPower += votingPower;
            }
        }
        // op == 2 (addAIAgent) был удален, т.к. AIAgents больше не управляются так в контракте
        if (op == 3) { // Создать предложение
            // require(sender() == self.chairman || self.members.exists(sender()), "Only chairman, members or AI agents can create proposals");
            // Для этой операции лучше использовать createProposal с ее логикой
            // Пропускаем здесь, чтобы избежать дублирования и потенциальных ошибок
        }
        if (op == 4) { // Проголосовать
            // require(self.members.exists(sender()) || self.aiAgents.exists(sender()), "Only members or AI agents can vote");
            // Для этой операции лучше использовать vote с ее логикой
            // Пропускаем здесь
        }
    }

    // --- Управление контрактом (Председателем/Владельцем) ---
    fun updateChairman(newChairman: Address) {
        self.requireOwner(); // Только текущий владелец (изначально первый chairman) может сменить председателя
        // Согласно Уставу 4.2, избрание Председателя - компетенция Общего собрания.
        // Эта функция - техническая передача прав председателя в контракте.
        // В идеале, ее вызов должен быть результатом решения Общего собрания.
        self.chairman = newChairman;
        // Рассмотреть вопрос: должен ли новый председатель также становиться owner?
        // Если да: self.transferOwnership(newChairman);
        // Пока оставляем owner неизменным, если chairman - это отдельная роль от owner'a OwnableTransferable.
        // Но в init они связаны. Логично, что chairman должен быть owner'ом.
        if (self.owner != newChairman) { // Если новый председатель не является текущим владельцем
             // Передаем также и владение контрактом (Ownable) новому председателю
             // Это важно, т.к. многие функции требуют self.owner
             send(SendParameters{
                to: self.owner, // Сообщение старому владельцу о передаче прав
                value: 0,
                body: "Ownership transfer initiated to new chairman".asComment(),
                mode: SendIgnoreErrors
             });
             self.transferOwnership(newChairman);
        }
        // TODO: Emit event ChairmanUpdated(newChairman)
    }

    fun updateVotingConfig(newQuorumPercent: Int, newDefaultVoteDurationDays: Int) {
        require(sender() == self.chairman, "ANOV2_ERR_ONLY_CHAIRMAN");
        require(newQuorumPercent > 0 && newQuorumPercent <= 100, "ANOV2_ERR_QUORUM_INVALID");
        require(newDefaultVoteDurationDays > 0, "ANOV2_ERR_DURATION_POSITIVE");
        self.votingConfig = VotingProcessConfig{
            quorumPercent: newQuorumPercent,
            defaultVotingDurationDays: newDefaultVoteDurationDays
        };
        // TODO: Emit event VotingConfigUpdated
    }

    get fun getVotingConfig(): VotingProcessConfig {
        return self.votingConfig;
    }

    get fun getChairman(): Address {
        return self.chairman;
    }
}
